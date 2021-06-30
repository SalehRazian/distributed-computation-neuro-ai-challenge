# Code Source: https://docs.dask.org/en/latest/setup/python-advanced.html
import asyncio
from dask.distributed import Worker


async def worker_function(scheduler_address):
    """
    This function starts the worker.
    :param scheduler_address: The address of the scheduler
    :return: None
    """
    worker = await Worker(scheduler_address)  # The worker is running
    await worker.finished()                   # Wait until the worker closes

# Change address when necessary
asyncio.get_event_loop().run_until_complete(worker_function("tcp://127.0.0.1:55062"))

