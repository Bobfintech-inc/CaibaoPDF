from typing import Iterable, List
from datetime import datetime

def batch_data(data: Iterable, batch_size: int) -> Iterable[List]:
    """
    Yield successive n-sized batches from the input iterable.

    Args:
        data: An iterable (e.g., list, generator) of data to be processed.
        batch_size: The size of each batch.

    Yields:
        A list containing a batch of data.
    """
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []  # Reset the batch after yielding
    # Yield the last batch if there's any leftover data
    if batch:
        yield batch


def get_task_id(file_hash):
    return f"{file_hash}_{datetime.now().isoformat(timespec='milliseconds') }"