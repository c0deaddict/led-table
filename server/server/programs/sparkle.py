from random import randint

from .base import Program
from ..settings import WIDTH, HEIGHT


class Sparkle(Program):
    fps = 60
    reset = False

    def __init__(self):
        self.initial = None
        self.prev = None

    async def start(self, initial):
        self.initial = initial

    async def animate(self, t):
        frame = dict()
        if self.prev:
            frame[self.prev] = self.initial[self.prev]

        x = randint(0, WIDTH - 1)
        y = randint(0, HEIGHT - 1)
        frame[(x, y)] = (255, 255, 255)

        self.prev = (x, y)
        return frame
