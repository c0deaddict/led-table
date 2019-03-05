import time

from ..log import logger
from ..settings import WIDTH, HEIGHT


class FakeLeds:
    def start(self):
        logger.info('Starting Fake LEDs (2 sec)')
        time.sleep(2)

    def stop(self):
        logger.info('Stopping Fake LEDs (1 sec)')
        time.sleep(1)

    def reset(self):
        logger.info('Resetting Fake LEDs (1 sec)')
        time.sleep(1)

    def paint(self, frame):
        num = 0
        for (x,y), color in frame.items():
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                num += 1

        logger.info(f'Painting Fake LEDs ({num} updates, .5 sec)')
        time.sleep(.5)


impl = FakeLeds()
