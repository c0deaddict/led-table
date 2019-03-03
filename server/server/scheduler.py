import asyncio
from datetime import datetime, timedelta

from .log import logger
from .leds import display
from .settings import CLAIM_EXPIRE
from .utils import Timer


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

    async def start(self):
        self.timer = Timer(5.0, self._timer_callback)
        logger.info('Scheduler started')

    async def stop(self):
        self.timer.cancel()
        logger.info('Scheduler stopped')

    async def _timer_callback(self):
        if self.client_id is not None:
            if self.claimed_at + CLAIM_EXPIRE < datetime.now():
                self.client_id = None
                self.claimed_at = None
        else:
            pass

    async def claim(self, client_id):
        if self.client_id == client_id:
            # Client already has the claim.
            self.claimed_at = datetime.now()
            return True
        elif self.client_id is None:
            self.client_id = client_id
            self.claimed_at = datetime.now()

            # TODO stop screensaver (if running).
            return True
        else:
            return False



scheduler = Scheduler()
