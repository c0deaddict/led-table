import board
import neopixel

from ..log import logger
from ..settings import WIDTH, HEIGHT
from .spiral import calc_spiral_coords

LED_PIN = board.D18
LED_PIXEL_ORDER = neopixel.GRB

assert WIDTH == HEIGHT
coords = calc_spiral_coords(WIDTH // 2)


class NeoStrip:
    def __init__(self):
        self.pixels = None

    def start(self):
        self.pixels = neopixel.NeoPixel(
            pin=LED_PIN,
            n=WIDTH*HEIGHT,
            auto_write=False,
            pixel_order=LED_PIXEL_ORDER,
        )
        self.reset()

    def stop(self):
        self.reset()
        self.pixels = None

    def reset(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def paint(self, frame):
        for (x,y), color in frame.items():
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                self.pixels[coords[(x, y)]] = color

        self.pixels.show()

    def read(self):
        result = dict()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                result[(x,y)] = self.pixels[coords[(x,y)]]
        return result


impl = NeoStrip()
