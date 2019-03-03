import time

from ..log import logger
from ..settings import WIDTH, HEIGHT


class FakeLeds:
    def start(self):
        logger.info('Starting Fake LEDs (4 sec)')
        time.sleep(4)

    def stop(self):
        logger.info('Stopping Fake LEDs (3 sec)')
        time.sleep(3)

    def paint(self, frame):
        num = 0
        for (x,y), color in frame.items():
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                num += 1

        logger.info(f'Painting Fake LEDs ({num} updates, 5 sec)')
        time.sleep(5)


impl = FakeLeds()
