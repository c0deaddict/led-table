import asyncio

from .log import logger


async def run_shell(command):
    p = await asyncio.create_subprocess_shell(command)
    await p.wait()
    if p.returncode != 0:
        logger.info('run_shell failed: {}'.format(command))


async def wait_until_done(task):
    while not task.done():
        await asyncio.sleep(.1)


# https://stackoverflow.com/a/45430833
class Timer:
    def __init__(self, timeout, callback, once=False):
        self.timeout = timeout
        self.callback = callback
        self.once = once
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while not self.once:
            await asyncio.sleep(self.timeout)
            await self.callback()

    def cancel(self):
        self._task.cancel()


def is_holiday(date):
    try:
        import holidays
        return date in holidays.Netherlands()
    except:
        return False
