import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .log import logger

# Make a single thread worker that processes updates to the LEDs.
# Write an async function that schedules work to be done in the worker.
# This is not a queue: only the most recent unpainted update is kept.
# TODO: add a FPS counter somewhere, and count the number of dropped frames.

class Worker:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.executor = None

    async def start(self):
        logger.info('Starting up LEDs')
        self.executor = ThreadPoolExecutor(max_workers=1)

    async def stop(self):
        logger.info('Shutting down LEDs')
        self.executor.shutdown()

    async def paint(self, frame):
        if self.lock.locked():
            logger.info('Dropping frame')
            return False

        loop = asyncio.get_running_loop()
        async with self.lock:
            print(loop)
            logger.info('Painting')
            await loop.run_in_executor(self.executor, self._paint, frame)

        logger.info('Done painting in async')
        return True


worker = Worker()


async def paint(frame):
    """Returns false if the paint was dropped."""
    return await worker.paint(frame)
