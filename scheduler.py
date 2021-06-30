# Code Source: https://docs.dask.org/en/latest/setup/python-advanced.html
import asyncio
from dask.distributed import Scheduler


async def scheduler_function():
    """
    This function starts the scheduler
    :return: None
    """
    scheduler = Scheduler(host="127.0.0.1", port=55062)        # Scheduler created, but not yet running - Change info where necessary
    scheduler = await scheduler                                # The scheduler is running
    await scheduler.finished()                                 # Wait until the scheduler closes

asyncio.get_event_loop().run_until_complete(scheduler_function())
