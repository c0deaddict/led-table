from random import randint

from .base import Program
from ..settings import WIDTH, HEIGHT


def rand_color():
    return (
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )


class Random(Program):
    fps = 60
    reset = True

    async def animate(self, t):
        x = randint(0, WIDTH - 1)
        y = randint(0, HEIGHT - 1)
        color = rand_color()
        return {(x, y): color}
