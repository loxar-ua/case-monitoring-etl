from math import ceil

from src.logger import logger

def batcher(batch_size: int):
    def decorator(func):
        def wrapper(size, *args, **kwargs):
            chunk_number = ceil(size / batch_size)

            for i in range(chunk_number):
                chunk_start = i * batch_size
                chunk_end = min((i + 1) * batch_size, size)

                batch_args = []
                for arg in args:
                    if isinstance(arg, (list, tuple)) and len(arg) == size:
                        batch_args.append(arg[chunk_start:chunk_end])
                    else:
                        batch_args.append(arg)

                current_real_size = chunk_end - chunk_start

                logger.info("Processing batch of size %s", current_real_size)
                batch_result = func(current_real_size, *batch_args, **kwargs)
                logger.info("Finished processing batch of size %s", current_real_size)

                if batch_result:
                    yield from batch_result
        return wrapper
    return decorator