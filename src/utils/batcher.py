from math import ceil
import numpy as np
from scipy.sparse import spmatrix
from src.logger import logger


def batcher(batch_size: int):
    def decorator(func):
        def wrapper(size, *args, **kwargs):
            if size <= 0:
                return None

            chunk_number = ceil(size / batch_size)

            all_results = []
            has_data = False

            for i in range(chunk_number):
                chunk_start = i * batch_size
                chunk_end = min((i + 1) * batch_size, size)

                batch_args = []
                for arg in args:
                    if isinstance(arg, (list, tuple, spmatrix, np.ndarray)) and len(arg) == size:
                        batch_args.append(arg[chunk_start:chunk_end])
                    else:
                        batch_args.append(arg)

                current_real_size = chunk_end - chunk_start

                logger.info(f"Processing batch {i + 1}/{chunk_number} (size {current_real_size})")

                batch_result = func(current_real_size, *batch_args, **kwargs)

                if batch_result is not None:
                    has_data = True
                    all_results.append(batch_result)

            logger.info("Batch processing complete.")

            if has_data:
                return all_results

            return None

        return wrapper

    return decorator