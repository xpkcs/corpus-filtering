




import ray, pandas as pd
from pathlib import Path
import pyarrow.csv as csv
import json




from typing import Dict, List



def format_system_prompt(labels: Dict[str, str]) -> str:
# You must only return a JSON array of strings where the elements are chosen from the list of keys in the label dictionary.

    return f'''
You are a classification model that labels documents based on a set of labels.
You will be given a document and a dictionary of labels. The keys are the labels and the values are the descriptions of the labels.
You will need to choose all labels that apply to the document.
You must return ONLY a JSON dictionary where the keys are the labels and the values are true or false if the label applies to the document
as described by the values in the label dictionary.
Do NOT include labels that are not present in the keys of the given label dictionary.
Do NOT include any other text in your response.
<labels>
{str(labels)}
</labels>
            '''


def format_prompt(system_prompt: str, prompt: str) -> List[Dict[str, str]]:

    return [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ]

def format_prompts(system_prompt: str, prompts: List[str]) -> List[List[Dict[str, str]]]:

    return [
        format_prompt(system_prompt, prompt)
        for prompt in prompts
    ]







import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import Dict, Any, Optional, List
import time


def load_model(model_name: str, quantization_config: Optional[BitsAndBytesConfig] = None):
    """
    Load Hugging Face model with default 8-bit quantization

    Returns:
        tuple: (model, tokenizer)
    """

    # Configure 8-bit quantization
    if not quantization_config:
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            # llm_int8_threshold=6.0,
            # llm_int8_has_fp16_weight=False,
        )

    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    print(f"Loading model {model_name} with 8-bit quantization...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
        # attn_implementation="flash_attention_2"
        # attn_implementation="eager",  # Use eager attention to avoid flash-attn requirement
        # low_cpu_mem_usage=True,
    )

    print("Model loaded successfully!")

    return model, tokenizer


def generate_batch_responses(batch_messages: List[List[Dict[str, str]]], model, tokenizer, max_new_tokens: int = 32) -> List[str]:
    """
    Generate responses for a batch of messages using batch inference

    Args:
        batch_messages: List of message lists, each containing message dictionaries with 'role' and 'content' keys
        model: The loaded Hugging Face model
        tokenizer: The loaded tokenizer
        max_new_tokens: Maximum number of new tokens to generate

    Returns:
        List of generated responses as strings
    """
    # Format all prompts in the batch
    formatted_prompts = []
    for messages in batch_messages:
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        formatted_prompts.append(formatted_prompt)

    # Tokenize all prompts with padding for batch processing
    inputs = tokenizer(
        formatted_prompts,
        return_tensors="pt",
        padding=True,  # Pad to the same length for batch processing
        truncation=True,
        max_length=tokenizer.model_max_length - max_new_tokens
    )

    # Move inputs to the same device as model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # Generate responses for the entire batch
    with torch.no_grad():
        try:
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,  # Greedy decoding
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                use_cache=False,  # Disable cache to avoid DynamicCache issues
            )
        except Exception as e:
            raise
            # print(f"Batch generation failed with error: {e}")
            # print("Trying alternative generation method...")
            # # Fallback: process one by one without batch
            # outputs = []
            # for i in range(inputs['input_ids'].shape[0]):
            #     single_input = {k: v[i:i+1] for k, v in inputs.items()}
            #     single_output = model.generate(
            #         **single_input,
            #         max_new_tokens=max_new_tokens,
            #         do_sample=False,
            #         pad_token_id=tokenizer.eos_token_id,
            #         eos_token_id=tokenizer.eos_token_id,
            #         use_cache=False,
            #     )
            #     outputs.append(single_output[0])
            # outputs = torch.stack(outputs)

    # Decode responses for each item in the batch
    responses = []
    input_lengths = inputs['input_ids'].shape[1]

    for i, output in enumerate(outputs):
        # For batch processing, we need to find the actual input length for each sequence
        # since they might be padded differently
        if 'attention_mask' in inputs:
            actual_input_length = inputs['attention_mask'][i].sum().item()
        else:
            actual_input_length = input_lengths

        # Decode only the new tokens (response)
        response = tokenizer.decode(
            output[actual_input_length:],
            skip_special_tokens=True
        )
        responses.append(response.strip())

    return responses

def process_batch(batch_df: pd.DataFrame, model, tokenizer) -> List[str]:
    """
    Process a batch of messages and generate responses using batch inference

    Args:
        batch_df: DataFrame containing 'messages' column
        model: The loaded model
        tokenizer: The loaded tokenizer

    Returns:
        List of generated responses
    """
    try:
        # Extract all messages from the batch
        batch_messages = batch_df['messages'].tolist()

        # Generate responses for the entire batch at once
        responses = generate_batch_responses(batch_messages, model, tokenizer)

        print(f"Processed batch of {len(responses)} items")
        return responses

    except Exception as e:
        print(f"Error processing batch: {e}")
        print("Falling back to individual processing...")

        # Fallback to individual processing if batch fails
        responses = []
        for idx, row in batch_df.iterrows():
            try:
                messages = [row['messages']]  # Convert to list for batch function
                response = generate_batch_responses(messages, model, tokenizer)[0]
                responses.append(response)
            except Exception as item_error:
                print(f"Error processing item {idx}: {item_error}")
                responses.append("")

        return responses



if __name__ == "__main__":



    ray.init(address='auto')




    LABELS = {
        'AI': 'Documents related to AI in general',
        'SFM': (
            'Documents related to self-fulfilling misalignment. '
            'These are documents that talk about the capabilities of AI that could cause harm to humans. '
            'The capabilities are not merely "you can use ML techniques to analyze...", but rather more like '
            '"AI systems exhibit deceptive capabilities that can be used to harm humans. Testing shows they '
            'will avoid being detected by standard safety checks or turned off by users." '
            'These documents are concerned about AI safety and alignment.'
        )
    }

    system_prompt = format_system_prompt(json.dumps(LABELS))

    model_name = "microsoft/Phi-3-mini-4k-instruct"
    model, tokenizer = load_model(model_name)

    ds = ray.data.read_csv(f'{Path(__file__).parents[1]}/keyword_filtering/matched.csv', parse_options=csv.ParseOptions(newlines_in_values=True))


    # Generate labels
    for batch_idx, batch in enumerate(ds.iter_batches(batch_size=1, batch_format='pandas')):

        print(f"Processing batch {batch_idx}...")

        # Format prompts for this batch
        batch['messages'] = format_prompts(system_prompt, batch['text'].tolist())

        # Generate responses for this batch
        responses = process_batch(batch, model, tokenizer)

        # Add responses to the batch
        batch['labels'] = responses

        # Optional: Print first response for verification
        if batch_idx == 0:
            print("-" * 50)
            print("Sample input message:")
            print(batch['text'].iloc[0])
            print("\nSample generated response:")
            print(responses[0])
            print("-" * 50)

        break

        # Optional: Save intermediate results or break for testing
        # Uncomment the break below to process only the first batch for testing
        # break

    print(f"Processed {batch_idx + 1} batches total.")

    # # Optional: Save results to file
    # results_df = pd.DataFrame({
    #     'labels': labels
    # })

    # output_path = f'{Path(__file__).parent}/labels.csv'
    # results_df.to_csv(output_path, index=False)
    # print(f"Results saved to {output_path}")
