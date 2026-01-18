from math import ceil

from src.logger import logger

def batcher(batch_size: int):
    def decorator(func):
        def wrapper(size, elements, *args, **kwargs):
            chunk_number = ceil(size / batch_size)

            for i in range(chunk_number):
                chunk_start = i * batch_size
                chunk_end = min((i + 1) * batch_size, size)
                current_chunk = elements[chunk_start:chunk_end]
                current_size = len(current_chunk)

                logger.info("Processing batch of size %s", current_size)
                batch_result = func(current_size, current_chunk, *args, **kwargs)
                logger.info("Finished processing batch of size %s", current_size)

                if batch_result:
                    yield from batch_result
        return wrapper
    return decorator