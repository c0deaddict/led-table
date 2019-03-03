import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .log import logger

# Make a single thread worker that processes updates to the LEDs.
# Write an async function that schedules work to be done in the worker.
# This is not a queue: only the most recent unpainted update is kept.
# TODO: add a FPS counter somewhere, and count the number of dropped frames.


# Spiral with the clock, starting right.
def calc_spiral_coords(size):
    result = dict()

    def emit(i, x, y):
        result[(x+size, y+size)] = i

    def enum_spiral(offset, n):
        if n == 0:
            emit(offset, 0, 0)
            enum_spiral(offset + 1, n + 1)
        elif n <= size:
            x = n
            y = n - 1
            i = offset
            emit(i, x, y)
            for j in range(0, 2*n-1):
                y = y - 1
                i = i + 1
                emit(i, x, y)
            for j in range(0, 2*n):
                x = x - 1
                i = i + 1
                emit(i, x, y)
            for j in range(0, 2*n):
                y = y + 1
                i = i + 1
                emit(i, x, y)
            for j in range(0, 2*n):
                x = x + 1
                i = i + 1
                emit(i, x, y)

            enum_spiral(i + 1, n + 1)

    enum_spiral(0, 0)
    return result



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

    def _start():
        

    def _paint(self, frame):
        logger.info('Painting... %s', str(frame))
        time.sleep(5)
        logger.info('Done painting in sync loop')


worker = Worker()


async def paint(frame):
    """Returns false if the paint was dropped."""
    return await worker.paint(frame)
