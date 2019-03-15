import time
import asyncio
from queue import Queue, Empty, Full
from threading import Thread, Event
from importlib import import_module

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
        self.impl = impl
        self.q = Queue(1)
        # TODO: add another queue that has a higher priority than self.q,
        # and which does not have a bound.
        self.stop_event = Event()
        self.worker = Thread(target=self._worker)
        self.loop = asyncio.get_event_loop()

    def _run(self, fn, args=[], resolve=None):
        try:
            self.q.put_nowait((lambda: fn(*args), resolve))
            return True
        except Full:
            return False

    async def _call(self, fn, args=[], fallback=None):
        future = asyncio.Future()
        def resolve(result):
            future.set_result(result)
        if self._run(fn, args, resolve):
            return await future
        else:
            return fallback

    async def start(self):
        logger.info('Starting up LEDs')
        self.worker.start()
        self._run(self.impl.start)

    async def stop(self):
        logger.info('Shutting down LEDs')
        self._run(self.impl.stop)
        self.stop_event.set()
        self.worker.join()

    async def reset(self):
        self._run(self.impl.reset)

    async def paint(self, frame):
        """
        Paint a frame. The frame can be a partial update to the LED
        display. Invalid coordinates are filtered out.

        Args:
            frame (dict): (x, y) => (r, g, b)

        Returns:
            True if the frame was painted, False it was dropped.

        """
        if not self._run(self.impl.paint, [frame]):
            logger.info('Dropping frame')
            return False

        return True

    async def read(self):
        return await self._call(self.impl.read, [], dict())

    def _worker(self):
        while not self.stop_event.is_set():
            try:
                fn, resolve = self.q.get(timeout=1.0)
                result = fn()
                if resolve:
                    self.loop.call_soon_threadsafe(resolve, result)
            except Empty:
                pass
