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
