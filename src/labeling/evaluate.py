import json
import re
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score, classification_report, confusion_matrix
import click




SCRIPT_DIR = Path(__file__).parent


def load_jsonl(jsonl_fp: Path) -> pd.DataFrame:

    with open(jsonl_fp, 'r') as f:
        df = [json.loads(line) for line in f]

    return pd.DataFrame(df)


def extract_json_from_string(s: str) -> dict:
    match = re.search(r'(\{.*\})', s, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            return None
    return None


def get_results_df(results_fp: Path) -> pd.DataFrame:
    df = load_jsonl(results_fp)
    idx = df['custom_id']
    df = pd.json_normalize(df['response'])
    df.index = idx
    return df



@click.group()
def cli():
    """Evaluate prompt responses."""
    pass



@cli.command()
@click.option(
    '--dataset-id', '-d',
    type=str,
    required=True
)
@click.option(
    '--results-dir', '-r',
    type=click.Path(exists=True, path_type=Path),
    default=SCRIPT_DIR / 'results'
)
@click.option(
    '--true-df-fp', '-t',
    type=click.Path(exists=True, path_type=Path),
    default=SCRIPT_DIR / 'Alignment Pretraing - High Quality Examples - Sheet1.csv'
)
def evaluate(dataset_id: str, results_dir: Path, true_df_fp: Path):

    df = get_results_df(results_dir / dataset_id / 'BIJOutputSet.jsonl')

    print('Responses:')
    df.info()

    responses_df = df.choices.apply(lambda _: _[0]['message'])
    print('\nResponses keys:')
    pd.json_normalize(responses_df).info()
    assert responses_df.apply(lambda _: 'content' in _).all(), 'Responses do not have a content key'


    pred_df = pd.json_normalize(df.choices.apply(lambda _: extract_json_from_string(_[0]['message']['content']))).astype({'label': 'int64'})
    pred_df.index = df.index


    true_df = pd.read_csv(
        true_df_fp,
        usecols=list(range(4)),
        header=0,
        names=['custom_id', 'source', 'label', 'text'],
        index_col='custom_id'
    )

    print('\nTrue labels:')
    true_df.info()
    print('\nPredicted labels:')
    pred_df.info()

    eval_df = true_df.merge(pred_df, left_index=True, right_index=True, suffixes=('_true', '_pred'))
    print('\nMerged labels:')
    eval_df.info()

    print('\nEvaluation results:')
    metrics = pd.Series({
        'accuracy': accuracy_score(eval_df['label_true'], eval_df['label_pred']),
        'precision': precision_score(eval_df['label_true'], eval_df['label_pred'], average='macro', zero_division=0),
        'recall': recall_score(eval_df['label_true'], eval_df['label_pred'], average='macro', zero_division=0),
        'f1': f1_score(eval_df['label_true'], eval_df['label_pred'], average='macro', zero_division=0),
        'fprecision': fbeta_score(eval_df['label_true'], eval_df['label_pred'], beta=0.5, average='macro', zero_division=0),
        'frecall': fbeta_score(eval_df['label_true'], eval_df['label_pred'], beta=2, average='macro', zero_division=0),
    })
    print(metrics)

    print('\n', classification_report(eval_df['label_true'], eval_df['label_pred'], labels=list(range(-1, 3)), zero_division=0))

    print('Evaluation results by label:')
    print(
        pd.DataFrame(
            confusion_matrix(eval_df['label_true'], eval_df['label_pred'], labels=list(range(-1, 3))),
            index=pd.Index(list(range(-1, 3)), name='label_true'),
            columns=pd.Index(list(range(-1, 3)), name='label_pred'),
        ).astype(int)
    )



    eval_df['label_0_or_1_true'] = eval_df['label_true'].apply(lambda _: _ in (0, 1))
    eval_df['label_0_or_1_pred'] = eval_df['label_pred'].apply(lambda _: _ in (0, 1))


    print('\n', classification_report(eval_df['label_0_or_1_true'], eval_df['label_pred'], labels=[False, True], zero_division=0))

    print('Evaluation results by label:')
    print(
        pd.DataFrame(
            confusion_matrix(eval_df['label_0_or_1_true'], eval_df['label_pred'], labels=list(range(-1, 3))),
            index=pd.Index(list(range(-1, 3)), name='label_0_or_1_true'),
            columns=pd.Index(list(range(-1, 3)), name='label_pred'),
        ).astype(int)
    )



    return eval_df



if __name__ == "__main__":
    cli()