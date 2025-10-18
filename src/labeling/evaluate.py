import json
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score, classification_report, confusion_matrix




SCRIPT_DIR = Path(__file__).parent


def load_jsonl(jsonl_fp: Path) -> pd.DataFrame:

    with open(jsonl_fp, 'r') as f:
        df = [json.loads(line) for line in f]

    return pd.DataFrame(df)


def evaluate():

    jsonl_fp = SCRIPT_DIR / 'results' / 'BIJOutputSet.jsonl'

    df = load_jsonl(jsonl_fp)
    idx = df['custom_id']
    df = pd.json_normalize(df['response'])
    df.index = idx

    print('Responses:')
    df.info()

    pred_df = pd.json_normalize(df['choices'].apply(lambda x: json.loads(x[0]['message']['content']))).astype({'label': 'int64'})
    pred_df.index = idx


    true_df = pd.read_csv(
        SCRIPT_DIR / 'Alignment Pretraining - 9_25 Annotation Test - Andy 10_7 200 Judgements .csv',
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
    # print(
    #     eval_df
    #         .groupby('label_true')['label_pred']
    #         .value_counts()
    #         .to_frame()
    #         .pivot_table(index='label_true', columns='label_pred', values='count', fill_value=0)
    #         .astype(int)
    # )
    print(
        pd.DataFrame(
            confusion_matrix(eval_df['label_true'], eval_df['label_pred'], labels=list(range(-1, 3))),
            index=pd.Index(list(range(-1, 3)), name='label_true'),
            columns=pd.Index(list(range(-1, 3)), name='label_pred'),
        ).astype(int)
    )





    return eval_df, metrics




if __name__ == "__main__":

    evaluate()