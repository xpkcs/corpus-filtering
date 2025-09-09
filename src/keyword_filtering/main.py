from typing import List, Tuple
import pandas as pd
import re
import numpy as np
import ray
import threading
import time
from ray.util.state import list_tasks, list_actors
import queue
from pathlib import Path
from itertools import islice
from tqdm import tqdm
from datasets import load_dataset

from concept import Concept, match_concept






@ray.remote
class ResultCollector:

    def __init__(self, output_path: str, buffer_size: int = 1000, batch_records: int = 1000):

        self.output_path = output_path
        self.buffer_size = buffer_size  # Maximum number of batches in queue
        self.batch_records = batch_records  # Records to accumulate before writing
        self.file = open(output_path, 'w')
        self._n_records = 0

        # Queue for buffering incoming data
        self.queue = queue.Queue(maxsize=buffer_size)

        # Start background writer thread
        self.writer_thread = threading.Thread(target=self._write_to_disk, daemon=False)
        self.writer_thread.start()

    def n_records(self) -> int:

        return self._n_records

    def write(self, batch: pd.DataFrame) -> None:
        """
        Non-blocking write - if queue has space,add to queue and return immediately,
        o/w block until space is available
        """

        if batch.shape[0] > 0:
            self.queue.put(batch)   # this is non-blocking if queue has space

    def _write_to_disk(self):
        """
        Background thread that continuously writes data from queue to disk.
        Accumulates data in memory until batch_records is reached or queue is empty.
        """

        accumulated_dfs = []
        accumulated_records = 0

        while True:
            try:
                # Get data from queue - this will raise ShutDown when queue is shutdown
                batch = self.queue.get()

                # Add to accumulation
                accumulated_dfs += [batch]
                accumulated_records += len(batch)

                # Mark task as done
                self.queue.task_done()


                if accumulated_records >= self.batch_records:
                    self._flush(accumulated_dfs, accumulated_records)
                    accumulated_dfs = []
                    accumulated_records = 0

            except queue.ShutDown:
                # Queue has been shutdown - flush any remaining data
                self._flush(accumulated_dfs, accumulated_records)
                print("Background writer shutting down gracefully")
                break

            except Exception as e:
                print(f"Error in background writer: {e}")
                raise

    def _flush(self, dfs_list: List[pd.DataFrame], total_records: int) -> None:
        """Flush accumulated DataFrames to disk"""

        if not dfs_list:
            return

        # Combine dfs and write to disk
        pd.concat(dfs_list, ignore_index=True).to_csv(self.file, index=False, header=self._n_records == 0, lineterminator='\n')
        self._n_records += total_records

        print(f"Wrote {total_records} records ({len(dfs_list)} batches)")

        # Force flush to disk
        self.file.flush()

    def close(self) -> None:
        """Shutdown background writer and close file"""

        print(f"Starting shutdown (queue size: {self.queue.qsize()})")

        # Shutdown queue gracefully - waits for all get() calls to finish
        self.queue.shutdown(immediate=False)
        print("Queue shutdown initiated")

        # Wait for the writer thread to finish
        print("Waiting for writer thread to finish...")
        self.writer_thread.join()

        if self.writer_thread.is_alive():
            print("WARNING: Writer thread did not shut down properly!")
        else:
            print("Writer thread finished successfully")

        self.file.close()
        print(f"File closed. Total records written: {self._n_records}")



@ray.remote
def match_keywords_worker(batch: pd.DataFrame, concept: Concept, collector: ResultCollector) -> None:
    '''Ray remote task to match documents in a batch against a concept'''

    mask = match_concept(batch['text'], concept)

    collector.write.remote(batch.loc[mask, ['id', 'text']])


def match_keywords(
    ds,
    concept: Concept,
    max_batches: int = 1000, # None
    batch_size: int = 1000,
    max_concurrent_tasks: int = 7       # num cpus - 1
) -> Tuple[ResultCollector, int]:

    futures = []

    concept_ref = ray.put(concept)
    collector = ResultCollector.remote('matched.csv')

    pbar = tqdm(islice(ds.iter(batch_size), max_batches), total=max_batches, desc='Keyword Filter', dynamic_ncols=True)
    for batch in pbar:

        futures += [match_keywords_worker.remote(batch, concept_ref, collector)]

        if len(futures) >= max_concurrent_tasks:
            done, futures = ray.wait(futures, num_returns=1)

    print(f"Waiting for {len(futures)} remaining Ray tasks to complete...")
    ray.get(futures)
    print("All Ray tasks completed successfully")

    print("Shutting down ResultCollector...")
    ray.get(collector.close.remote())
    print("ResultCollector shutdown complete")

    return collector, pbar.n * batch_size




if __name__ == '__main__':

    ray.init(address='auto', include_dashboard=True, dashboard_port=8265)


    corpus_hf_ds = load_dataset("EleutherAI/dclm-dedup-25B", streaming=True)


    concept = Concept.from_yaml(f'{Path(__file__).parent}/concepts/alignment.yaml')


    print("Starting keyword matching process...")
    collector, n_documents = match_keywords(
        corpus_hf_ds['train'].select_columns(['id', 'text']).with_format('pandas'),
        concept,
        max_batches=100,
        batch_size=10000,
        max_concurrent_tasks=15
    )

    n_documents_matched = ray.get(collector.n_records.remote())
    print(f'Wrote {n_documents_matched} documents out of {n_documents}: {n_documents_matched / n_documents * 100:.2f}%')


    # print("Shutting down Ray...")
    # ray.shutdown()