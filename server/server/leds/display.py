import time
import asyncio
from importlib import import_module

from concurrent.futures import ThreadPoolExecutor

from .. import settings
from ..log import logger


class Display:
    """
    Make a single thread worker that processes updates to the LEDs.
    Write an async function that schedules work to be done in the worker.
    This is not a queue: only the most recent unpainted update is kept.
    TODO: add a FPS counter somewhere, and count the number of dropped frames.
    """
    def __init__(self, impl):
        self.loop = None
        self.executor = None
        self.lock = asyncio.Lock()
        self.impl = impl

    async def _run(self, fn, *args):
        return await self.loop.run_in_executor(self.executor, fn, *args)

    async def start(self):
        logger.info('Starting up LEDs')
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)
        await self._run(self.impl.start)

    async def stop(self):
        logger.info('Shutting down LEDs')
        await self._run(self.impl.stop)
        self.executor.shutdown()
        self.executor = None
        self.loop = None

    async def reset(self):
        await self._run(self.impl.reset)

    async def paint(self, frame):
        """
        Paint a frame. The frame can be a partial update to the LED
        display. Invalid coordinates are filtered out.

        Args:
            frame (dict): (x, y) => (r, g, b)

        Returns:
            True if the frame was painted, False it was dropped.

        """
        if self.lock.locked():
            logger.info('Dropping frame')
            return False

        async with self.lock:
            await self._run(self.impl.paint, frame)

        return True

    async def read(self):
        return await self._run(self.impl.read)
