# Code Source: https://docs.dask.org/en/latest/setup/python-advanced.html
import asyncio
from dask.distributed import Scheduler


async def scheduler_function():
    """
    This function starts the scheduler
    :return: None
    """
    s = Scheduler(host="192.168.1.117", port=55063)        # Scheduler created, but not yet running - Change info where necessary
    s = await s                                            # The scheduler is running
    await s.finished()                                     # Wait until the scheduler closes

asyncio.get_event_loop().run_until_complete(scheduler_function())
