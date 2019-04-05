import asyncio
from datetime import datetime, timedelta

from .log import logger
from .leds import display
from .settings import (
    CLAIM_EXPIRE,
    SCHEDULE_ON_TIME,
    SCHEDULE_ON_WEEKENDS,
    SCHEDULE_ON_HOLIDAYS,
)
from .utils import Timer, is_holiday
from .screensaver import MaybeScreensaverLoop


def in_schedule(dt):
    if is_holiday(dt):
        return False

    # 0 = mon, ... 5 = sat, 6 = sun
    if not SCHEDULE_ON_HOLIDAYS and dt.weekday() in [5, 6]:
        return False

    start, end = SCHEDULE_ON_TIME
    return start <= dt.time() < end


class Scheduler:
    """
    The scheduler arbitrates access to the display. Only one client
    can have access to the display at any given moment in time. After
    a <certain> amount of time a client's claim is expired and must
    be renewed.

    If no client has claimed the display, and <certain> criteria are
    met, the screensaver is started. It is stopped as soon as a client
    does a claim.
    """

    def __init__(self):
        self.client_id = None
        self.claimed_at = None
        self.timer = None
        self.screensaver = None

    async def start(self):
        self.timer = Timer(5.0, self._timer_callback)
        self.screensaver = MaybeScreensaverLoop()
        await self.screensaver.start()
        logger.info('Scheduler: started')

    async def stop(self):
        self.timer.cancel()
        self.timer = None
        await self.screensaver.stop()
        self.screensaver = None
        logger.info('Scheduler: stopped')

    async def _timer_callback(self):
        if not in_schedule(datetime.now()):
            await self._sleep()
        elif self.client_id is not None:
            if self.claimed_at + CLAIM_EXPIRE < datetime.now():
                logger.info('Scheduler: {0} idled and released the display'.format(self.client_id))
                await self._release()

    async def claim(self, client_id):
        # Reject claims outside "ON" schedule.
        if not in_schedule(datetime.now()):
            return False

        if self.client_id == client_id:
            # Client already has the claim, extend the claim.
            self.claimed_at = datetime.now()
            return True
        elif self.client_id is None:
            self.client_id = client_id
            self.claimed_at = datetime.now()
            logger.info('Scheduler: {0} claimed the display'.format(self.client_id))
            await self.screensaver.stop()
            return True
        else:
            return False

    async def release(self, client_id):
        if self.client_id != client_id:
            logger.info('Scheduler: client {0} tried to release without a claim'.format(client_id))
        else:
            await self._release()

    async def _release(self):
        self.client_id = None
        self.claimed_at = None
        await self.screensaver.start()

    async def _sleep(self):
        self.client_id = None
        self.claimed_at = None
        await self.screensaver.stop()
        await display.reset()


scheduler = Scheduler()
