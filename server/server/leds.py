from .log import logger

# Make a single thread worker that processes updates to the LEDs.
# Write an async function that schedules work to be done in the worker.
# This is not a queue: only the most recent unpainted update is kept.
# TODO: add a FPS counter somewhere, and count the number of dropped frames.


async def start():
    logger.info('Starting up LEDs')


async def stop():
    logger.info('Shutting down LEDs')


async def paint():
    """Returns false if the paint was dropped."""
    return False


