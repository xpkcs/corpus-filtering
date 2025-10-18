import json
import pprint
from typing import Any
import pandas as pd
from pathlib import Path
import click
import requests
import os

from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = Path(__file__).parent


def load_prompt_templates(system_prompt_tmpl_fp: Path, user_prompt_tmpl_fp: Path) -> tuple[str, str]:

    with open(system_prompt_tmpl_fp, 'r') as infl:
        system_prompt_tmpl = infl.read()

    with open(user_prompt_tmpl_fp, 'r') as infl:
        user_prompt_tmpl = infl.read()

    return system_prompt_tmpl, user_prompt_tmpl


def prepare_message(row: pd.Series, system_prompt_tmpl: str, user_prompt_tmpl: str) -> dict[str, Any]:

    return {
        "custom_id": row.id,
        "body": {
            "messages": [
                {"role": "system", "content": system_prompt_tmpl},
                {"role": "user", "content": user_prompt_tmpl.format(text=row.text)}
            ],
            "temperature": 0,
            "max_tokens": 2048
        }
    }


def check_jsonl_for_invalid_syntax(jsonl_fp: Path) -> None:

    n_invalid_lines = 0

    with open(jsonl_fp, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {i}: Invalid - {e}")
                print(f"Problem at character {e.pos}")
                n_invalid_lines += 1

        print(f"Done validating file {jsonl_fp} | {n_invalid_lines} / {i} invalid lines")


class FireworksClient:
    """Client for interacting with Fireworks AI API."""

    def __init__(self, account_id: str, api_key: str):
        """Initialize the Fireworks AI client.

        Args:
            account_id: Fireworks AI account ID
            api_key: Fireworks AI API key
        """
        self.account_id = account_id
        self.api_key = api_key
        self.base_url = "https://api.fireworks.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_dataset(self, dataset_id: str) -> dict:
        """Create a dataset in Fireworks AI.

        Args:
            dataset_id: ID for the dataset to create

        Returns:
            API response as dictionary

        Raises:
            Exception: If dataset creation fails
        """
        response = requests.post(
            f"{self.base_url}/accounts/{self.account_id}/datasets",
            headers=self.headers,
            json={
                "datasetId": dataset_id,
                "dataset": {"userUploaded": {}}
            }
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create dataset: {response.status_code} - {response.text}")

        return response.json()

    def upload_file(self, dataset_id: str, jsonl_fp: Path) -> dict:
        """Upload a JSONL file to a Fireworks AI dataset.

        Args:
            dataset_id: ID of the dataset to upload to
            jsonl_fp: Path to the JSONL file to upload

        Returns:
            API response as dictionary

        Raises:
            Exception: If file upload fails
        """
        upload_headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        with open(jsonl_fp, "rb") as f:
            files = {"file": f}
            response = requests.post(
                f"{self.base_url}/accounts/{self.account_id}/datasets/{dataset_id}:upload",
                headers=upload_headers,
                files=files
            )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")

        return response.json()

    def delete_dataset(self, dataset_id: str) -> dict:
        """Delete a dataset in Fireworks AI.

        Args:
            dataset_id: ID of the dataset to delete

        Returns:
            API response as dictionary

        Raises:
            Exception: If dataset deletion fails
        """
        response = requests.delete(
            f"{self.base_url}/accounts/{self.account_id}/datasets/{dataset_id}",
            headers=self.headers
        )

        if response.status_code not in [200, 201, 204]:
            raise Exception(f"Failed to delete dataset: {response.status_code} - {response.text}")

        # Some delete operations return empty response body
        try:
            return response.json()
        except ValueError:
            return {"status": "success", "message": "Dataset deleted successfully"}

    def update_dataset(self, dataset_id: str, **kwargs) -> dict:
        """Update a dataset in Fireworks AI.

        Args:
            dataset_id: ID of the dataset to update
            **kwargs: Additional fields to update (displayName, exampleCount, etc.)

        Returns:
            API response as dictionary

        Raises:
            Exception: If dataset update fails
        """
        # Build payload with provided fields
        payload = {}
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = value

        response = requests.patch(
            f"{self.base_url}/accounts/{self.account_id}/datasets/{dataset_id}",
            headers=self.headers,
            json=payload
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to update dataset: {response.status_code} - {response.text}")

        return response.json()

    def get_batch_job_status(self, batch_id: str) -> dict:
        """Get the status of a batch inference job.

        Args:
            batch_id: ID of the batch inference job

        Returns:
            API response as dictionary containing job status

        Raises:
            Exception: If status retrieval fails
        """
        response = requests.get(
            f"https://api.fireworks.ai/v1/accounts/{self.account_id}/batchInferenceJobs/{batch_id}",
            headers={"Authorization": self.api_key}
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to get batch job status: {response.status_code} - {response.text}")

        return response.json()

    def get_download_endpoint(self, dataset_id: str) -> dict:
        """Get download endpoint for a dataset.

        Args:
            dataset_id: ID of the dataset to download

        Returns:
            API response containing download URLs

        Raises:
            Exception: If download endpoint retrieval fails
        """
        response = requests.get(
            f"{self.base_url}/accounts/{self.account_id}/datasets/{dataset_id}:getDownloadEndpoint",
            headers=self.headers,
            json={}
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to get download endpoint: {response.status_code} - {response.text}")

        return response.json()

    def download_dataset(self, dataset_id: str, output_dir: Path = None) -> list[Path]:
        """Download all files from a dataset.

        Args:
            dataset_id: ID of the dataset to download
            output_dir: Directory to save files (defaults to current directory)

        Returns:
            List of downloaded file paths

        Raises:
            Exception: If download fails
        """
        if output_dir is None:
            output_dir = Path.cwd()
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Get download endpoint
        download_info = self.get_download_endpoint(dataset_id)

        if 'filenameToSignedUrls' not in download_info:
            raise Exception("No download URLs found in response")

        downloaded_files = []

        for object_path, signed_url in download_info['filenameToSignedUrls'].items():
            filename = Path(object_path).name
            output_path = output_dir / filename

            # Download file
            file_response = requests.get(signed_url)
            if file_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(file_response.content)
                downloaded_files.append(output_path)
            else:
                raise Exception(f"Failed to download {filename}: {file_response.status_code}")

        return downloaded_files

    def create_batch_job(
        self,
        job_id: str,
        model: str,
        input_dataset_id: str,
        output_dataset_id: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> dict:
        """Create a batch inference job in Fireworks AI.

        Args:
            job_id: ID for the batch inference job
            model: Model to use for inference
            input_dataset_id: ID of the input dataset
            output_dataset_id: ID of the output dataset
            max_tokens: Maximum tokens for inference
            temperature: Temperature for inference
            top_p: Top-p for inference

        Returns:
            API response as dictionary

        Raises:
            Exception: If batch job creation fails
        """
        response = requests.post(
            f"{self.base_url}/accounts/{self.account_id}/batchInferenceJobs?batchInferenceJobId={job_id}",
            headers=self.headers,
            json={
                "model": model,
                "inputDatasetId": f"accounts/{self.account_id}/datasets/{input_dataset_id}",
                "outputDatasetId": f"accounts/{self.account_id}/datasets/{output_dataset_id}",
                "inferenceParameters": {
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                    "topP": top_p
                }
            }
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create batch job: {response.status_code} - {response.text}")

        return response.json()

    def submit_batch_inference(
        self,
        input_file: Path,
        input_dataset_id: str = "batch-input-dataset",
        output_dataset_id: str = "batch-output-dataset",
        job_id: str = "llm-labeling",
        model: str = "accounts/fireworks/models/gpt-oss-120b",
        max_tokens: int = 2048,
        temperature: float = 0.0,
        top_p: float = 0.9,
        skip_dataset_creation: bool = False
    ) -> dict:
        """Complete workflow to submit a batch inference job.

        Args:
            input_file: Path to the JSONL file to process
            input_dataset_id: ID for the input dataset
            output_dataset_id: ID for the output dataset
            job_id: ID for the batch inference job
            model: Model to use for inference
            max_tokens: Maximum tokens for inference
            temperature: Temperature for inference
            top_p: Top-p for inference
            skip_dataset_creation: Whether to skip creating datasets

        Returns:
            Final batch job response as dictionary

        Raises:
            Exception: If any step in the workflow fails
        """
        # Create input dataset
        if not skip_dataset_creation:
            self.create_dataset(input_dataset_id)

        # Upload file to input dataset
        try:
            self.upload_file(input_dataset_id, input_file)
        except Exception as upload_error:
            # If upload fails, it might be because data was already uploaded
            # Try to update the dataset instead
            error_msg = str(upload_error).lower()
            if "dataset is already uploaded" in error_msg:
                # Update the dataset with new data
                self.update_dataset(input_dataset_id, userUploaded={})
            else:
                # Re-raise if it's a different type of error
                raise upload_error

        # Create batch inference job
        return self.create_batch_job(
            job_id=job_id,
            model=model,
            input_dataset_id=input_dataset_id,
            output_dataset_id=output_dataset_id,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )



@click.group()
def cli():
    """Batch inference tool for preparing prompts from corpus data."""
    pass


@cli.command()
@click.option('--system-prompt', '-s',
              type=click.Path(exists=True, path_type=Path),
              default=SCRIPT_DIR / 'system_prompt.txt',
              help='Path to system prompt template file')
@click.option('--user-prompt', '-u',
              type=click.Path(exists=True, path_type=Path),
              default=SCRIPT_DIR / 'user_prompt.txt',
              help='Path to user prompt template file')
@click.option('--corpus', '-c',
              type=click.Path(exists=True, path_type=Path),
              default=SCRIPT_DIR / 'Alignment Pretraining - 9_25 Annotation Test - Andy 10_7 200 Judgements .csv',
              help='Path to corpus CSV file')
@click.option('--output', '-o',
              type=click.Path(path_type=Path),
              default=SCRIPT_DIR / 'prompts.jsonl',
              help='Output path for prompts JSONL file')
@click.option('--limit', '-l',
              type=int,
              help='Limit number of prompts to process (for testing)')
def prepare(system_prompt: Path, user_prompt: Path, corpus: Path, output: Path, limit: int):
    """Prepare prompts from corpus data using prompt templates."""

    click.echo(f"Loading prompt templates from {system_prompt} and {user_prompt}")
    system_prompt_tmpl, user_prompt_tmpl = load_prompt_templates(system_prompt, user_prompt)

    click.echo(f"Loading corpus from {corpus}")
    corpus_df = pd.read_csv(
        corpus,
        usecols=list(range(4)),
        header=0,
        names=['id', 'source', 'label', 'text']
    )

    if limit:
        corpus_df = corpus_df.head(limit)
        click.echo(f"Limited to {limit} rows for processing")

    corpus_df.info()

    click.echo("Preparing prompts...")
    prompts = corpus_df.apply(
        prepare_message,
        system_prompt_tmpl=system_prompt_tmpl,
        user_prompt_tmpl=user_prompt_tmpl,
        axis=1
    ).rename('prompts')

    prompts.info()
    click.echo("Sample prompts:")
    click.echo(prompts.head())

    click.echo(f"Writing prompts to {output}")
    with open(output, 'w') as outfl:
        for item in prompts:
            outfl.write(json.dumps(item) + '\n')

    click.echo("Validating output file...")
    check_jsonl_for_invalid_syntax(output)


@cli.command()
@click.argument('jsonl_fp', type=click.Path(exists=True, path_type=Path))
def validate(jsonl_fp: Path):
    """Validate a JSONL file for invalid JSON syntax."""
    click.echo(f"Validating {jsonl_fp}")
    check_jsonl_for_invalid_syntax(jsonl_fp)


@cli.command()
@click.option('--input-file', '-i',
              type=click.Path(exists=True, path_type=Path),
              required=True,
              help='Path to input JSONL file to upload')
@click.option('--account-id', '-a',
              envvar='FIREWORKS_ACCOUNT_ID',
              help='Fireworks AI account ID (can also be set via ACCOUNT_ID env var)')
@click.option('--api-key', '-k',
              envvar='FIREWORKS_API_KEY',
              help='Fireworks AI API key (can also be set via API_KEY env var)')
@click.option('--model', '-m',
              default='accounts/fireworks/models/gpt-oss-120b',
              help='Model to use for batch inference')
@click.option('--input-dataset-id', '-d',
              default='batch-input-dataset',
              help='Input dataset ID')
@click.option('--output-dataset-id', '-o',
              default='batch-output-dataset',
              help='Output dataset ID')
@click.option('--job-id', '-j',
              default='llm-labeling',
              help='Batch inference job ID')
@click.option('--max-tokens', '-t',
              type=int,
              default=2048,
              help='Maximum tokens for inference')
@click.option('--temperature', '-temp',
              type=float,
              default=0.,
              help='Temperature for inference')
@click.option('--top-p', '-p',
              type=float,
              default=0.9,
              help='Top-p for inference')
@click.option('--skip-dataset-creation', '-s',
              is_flag=True,
              help='Skip creating datasets (assume they already exist)')
def submit_fireworks(
    input_file: Path,
    account_id: str,
    api_key: str,
    model: str,
    input_dataset_id: str,
    output_dataset_id: str,
    job_id: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    skip_dataset_creation: bool
):
    """Submit a batch inference job to Fireworks AI."""

    # Validate required credentials
    if not account_id:
        raise click.ClickException("Account ID is required. Set ACCOUNT_ID env var or use --account-id option.")
    if not api_key:
        raise click.ClickException("API key is required. Set API_KEY env var or use --api-key option.")

    try:
        # Validate input file first
        click.echo(f"Validating input file: {input_file}")
        check_jsonl_for_invalid_syntax(input_file)

        # Initialize Fireworks client
        client = FireworksClient(account_id, api_key)

        # Submit batch inference using the client
        click.echo("Submitting batch inference job to Fireworks AI...")
        job_result = client.submit_batch_inference(
            input_file=input_file,
            input_dataset_id=input_dataset_id,
            output_dataset_id=output_dataset_id,
            job_id=job_id,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            skip_dataset_creation=skip_dataset_creation
        )

        click.echo("✅ Batch inference job submitted successfully!")
        click.echo(f"Job details: {job_result}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.ClickException(f"Failed to submit batch job: {str(e)}")


@cli.command()
@click.option('--dataset-id', '-d',
              required=True,
              help='Dataset ID to delete')
@click.option('--account-id', '-a',
              envvar='FIREWORKS_ACCOUNT_ID',
              help='Fireworks AI account ID (can also be set via FIREWORKS_ACCOUNT_ID env var)')
@click.option('--api-key', '-k',
              envvar='FIREWORKS_API_KEY',
              help='Fireworks AI API key (can also be set via FIREWORKS_API_KEY env var)')
@click.option('--confirm', '-y',
              is_flag=True,
              help='Skip confirmation prompt')
def delete_dataset(dataset_id: str, account_id: str, api_key: str, confirm: bool):
    """Delete a dataset from Fireworks AI."""

    # Validate required credentials
    if not account_id:
        raise click.ClickException("Account ID is required. Set FIREWORKS_ACCOUNT_ID env var or use --account-id option.")
    if not api_key:
        raise click.ClickException("API key is required. Set FIREWORKS_API_KEY env var or use --api-key option.")

    # Confirmation prompt
    if not confirm:
        if not click.confirm(f"Are you sure you want to delete dataset '{dataset_id}'? This action cannot be undone."):
            click.echo("Operation cancelled.")
            return

    try:
        # Initialize Fireworks client
        client = FireworksClient(account_id, api_key)

        # Delete the dataset
        click.echo(f"Deleting dataset: {dataset_id}")
        result = client.delete_dataset(dataset_id)

        click.echo("✅ Dataset deleted successfully!")
        click.echo(f"Result: {result}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.ClickException(f"Failed to delete dataset: {str(e)}")


@cli.command()
@click.option('--batch-id', '-b',
              required=True,
              help='Batch inference job ID to check')
@click.option('--account-id', '-a',
              envvar='FIREWORKS_ACCOUNT_ID',
              help='Fireworks AI account ID (can also be set via FIREWORKS_ACCOUNT_ID env var)')
@click.option('--api-key', '-k',
              envvar='FIREWORKS_API_KEY',
              help='Fireworks AI API key (can also be set via FIREWORKS_API_KEY env var)')
def batch_status(batch_id: str, account_id: str, api_key: str):
    """Check the status of a batch inference job."""

    # Validate required credentials
    if not account_id:
        raise click.ClickException("Account ID is required. Set FIREWORKS_ACCOUNT_ID env var or use --account-id option.")
    if not api_key:
        raise click.ClickException("API key is required. Set FIREWORKS_API_KEY env var or use --api-key option.")

    try:
        # Initialize Fireworks client
        client = FireworksClient(account_id, api_key)

        # Get batch job status
        click.echo(f"Checking status for batch job: {batch_id}")
        status = client.get_batch_job_status(batch_id)

        click.echo("✅ Batch job status retrieved successfully!")
        click.echo(f"Status:\n{pprint.pformat(status)}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.ClickException(f"Failed to get batch job status: {str(e)}")


@cli.command()
@click.option('--dataset-id', '-d',
              default='batch-output-dataset',
              help='Dataset ID to download results from')
@click.option('--output-dir', '-o',
              default=SCRIPT_DIR / 'results',
              type=click.Path(path_type=Path),
              help='Output directory to save files (defaults to script directory)')
@click.option('--account-id', '-a',
              envvar='FIREWORKS_ACCOUNT_ID',
              help='Fireworks AI account ID (can also be set via FIREWORKS_ACCOUNT_ID env var)')
@click.option('--api-key', '-k',
              envvar='FIREWORKS_API_KEY',
              help='Fireworks AI API key (can also be set via FIREWORKS_API_KEY env var)')
def download_dataset(dataset_id: str, output_dir: Path, account_id: str, api_key: str):
    """Download results from a dataset."""

    # Validate required credentials
    if not account_id:
        raise click.ClickException("Account ID is required. Set FIREWORKS_ACCOUNT_ID env var or use --account-id option.")
    if not api_key:
        raise click.ClickException("API key is required. Set FIREWORKS_API_KEY env var or use --api-key option.")

    try:
        # Initialize Fireworks client
        client = FireworksClient(account_id, api_key)

        # Download results
        click.echo(f"Downloading results from dataset: {dataset_id}")
        if output_dir:
            click.echo(f"Output directory: {output_dir}")

        downloaded_files = client.download_dataset(dataset_id, output_dir)

        click.echo("✅ Results downloaded successfully!")
        click.echo(f"Downloaded {len(downloaded_files)} files:")
        for file_path in downloaded_files:
            click.echo(f"  - {file_path}")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        raise click.ClickException(f"Failed to download results: {str(e)}")


if __name__ == '__main__':
    cli()
