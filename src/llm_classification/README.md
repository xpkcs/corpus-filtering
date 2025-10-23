# LLM Classification Using Fireworks AI

## Setup

Create a virtual env and install `./requirements-minimal.txt`

`cd` to this directory (`./src/llm_classification`) and run commands from here.

Create a `.env` file in this directory containing your fireworks account info:

```sh
export FIREWORKS_ACCOUNT_ID=""
export FIREWORKS_API_KEY=""
```

## Usage

### CLI

There are two CLIs, `fireworks` and `evaluate`. Assuming you're in this directory, run `fireworks.py --help` and `evaluate.py` to print help messages.

Download a `.csv` containing the documents you want to generate outputs for.
Expected columns (in order, column names don't have to match exactly but order does):
    - custom_id
    - source
    - label
    - text

Run the `prepare` CLI command to apply the system/user prompts to each document and generate the expected `.jsonl` file.

```sh
./fireworks.py prepare -s ./prompts/system_prompt3.md -c ${PATH_TO_CORPUS_CSV}
```

This will generate a `prompts.jsonl` file in the same directory as the `fireworks.py` file, or you can change the filepath with the `-o` command.

Submit the batch job to fireworks:

```sh
./fireworks.py submit-fireworks \
    -i ./prompts.jsonl \
    -d highq-qwen3-235b-a22b-instruct-2507-input-v3 \
    -o highq-qwen3-235b-a22b-instruct-2507-output-v3 \
    -j highq-qwen3-235b-a22b-instruct-2507-v3 \
    -m accounts/fireworks/models/qwen3-235b-a22b-instruct-2507
```

Fireworks is kinda finnicky about dataset/batch job names. Each time you run a batch job both the batch job and output dataset must not exist. You can delete the output dataset using the `fireworks.py` CLI but you have to manually delete the batch job in the UI. My naming convention for datasets is `${TYPE_OF_DATASET}-${MODEL}-[input|output]-${SYSTEM_PROMPT_VERSION}` and similar for the batch job.

You can skip needing to delete and recreate the input dataset with the `-s` flag. `-m` is the model ID as found in the Fireworks UI.

Download the output dataset (containing model responses):

```sh
./fireworks.py download-dataset -d highq-qwen3-235b-a22b-instruct-2507-output-v3
```

This will save the dataset in a folder in the same directory as the `fireworks.py` script called `results/highq-qwen3-235b-a22b-instruct-2507-output-v3`. The responses are in the `BIJOutputSet.jsonl` file there.

Evaluate the dataset:

```sh
./evaluate.py evaluate -d highq-qwen3-235b-a22b-instruct-2507-output-v3
```

Double check that the `-t` flag points to the same file containing the human labeled documents `${PATH_TO_CORPUS_CSV}` that we ran in the `prepare` command.

The console will output classification reports!