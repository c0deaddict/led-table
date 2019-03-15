from random import randint

from .base import Program
from ..settings import WIDTH, HEIGHT


def rand_color():
    return (
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )


class FullRand(Program):
    fps = 20
    reset = True

    async def animate(self, t):
        color = rand_color()
        frame = dict()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                frame[(x, y)] = color
        return frame
