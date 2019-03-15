from random import randint, choice
from enum import Enum

from .base import Program
from ..settings import WIDTH, HEIGHT


def rand_color():
    return (
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )


class Dir(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Sweep(Program):
    fps = 20
    reset = False

    def __init__(self):
        self.initial = None
        self.current_dir = None
        self.color = None

    async def start(self, initial):
        self.initial = initial

    async def animate(self, t):
        i = t % WIDTH
        if i == 0:
            self.current_dir = None

        if self.current_dir is None:
            self.current_dir = choice(list(Dir))
            self.color = rand_color()

        frame = dict()
        if self.current_dir == Dir.NORTH:
            for x in range(WIDTH):
                frame[(x, HEIGHT-1-i)] = self.color
        elif self.current_dir == Dir.SOUTH:
            for x in range(WIDTH):
                frame[(x, i)] = self.color
        elif self.current_dir == Dir.EAST:
            for y in range(HEIGHT):
                frame[(i, y)] = self.color
        elif self.current_dir == Dir.WEST:
            for y in range(HEIGHT):
                frame[(WIDTH-1-i, y)] = self.color

        return frame
