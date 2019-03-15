import asyncio
import time
from datetime import datetime, timedelta
from random import choice

from .log import logger
from .leds import display
from .settings import (
    SCREENSAVER_CHANGE,
    SCREENSAVER_ON_CHANCE,
    SCREENSAVER_ON_MIN_WINDOW,
)

from .programs import programs


class Screensaver:
    """
    Cycles randomly through various screensaver programs.
    """
    task = None
    prog = None
    start_prog = None
    timeout = None
    lock = asyncio.Lock()
    t = None

    async def start(self):
        if self.task is None:
            # Need a lock to ensure _loop doesn't run before self.prog
            # has been properly initialized.
            async with self.lock:
                self.task = asyncio.ensure_future(self._loop())
                await self.next_prog()
            logger.info('Screensaver started')

    async def stop(self):
        if self.task:
            self.task.cancel()
            self.task = None
            self.prog = None
            self.start_prog = None
            self.timeout = None
            self.t = None
            logger.info('Screensaver stopped')

    async def next_prog(self):
        Prog = choice(programs)
        logger.info('Starting screensaver program: {0}'.format(Prog))
        self.prog = Prog()
        self.start_prog = datetime.now()
        self.timeout = 1.0 / self.prog.fps
        self.t = 0
        if self.prog.reset:
            await display.reset()
            initial = dict()
        else:
            initial = await display.read()
        await self.prog.start(initial)

    async def _loop(self):
        while True:
            async with self.lock:
                if datetime.now() - self.start_prog > SCREENSAVER_CHANGE:
                    await self.next_prog()

                start = time.time()
                frame = await self.prog.animate(self.t)
                await display.paint(frame)
                self.t += 1
                elapsed = time.time() - start
                timeout = self.timeout - elapsed
                if timeout > 0:
                    await asyncio.sleep(timeout)
                else:
                    logger.info('Screensaver lagging')


class MaybeScreensaver(Screensaver):
    """
    Maybe start screensaver.
    TODO implement.
    TODO have a way to set 'no program' on the screensaver
         (it should display reset when no program).
    """
    async def start(self):
        await super().start()

    async def stop(self):
        await super().stop()
