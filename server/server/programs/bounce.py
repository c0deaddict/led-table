from random import randint

from .base import Program
from ..settings import WIDTH, HEIGHT


def rand_color():
    return (
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )


class Box(object):
    x = 0
    y = 0
    w = 2
    h = 2
    dx = 0
    dy = 0
    color = 0


class Bounce(Program):
    fps = 30
    n = 5
    reset = True

    def __init__(self):
        self.objects = []
        for i in range(self.n):
            b = Box()
            b.w = 2
            b.h = 2
            b.x = randint(0, WIDTH - b.w)
            b.y = randint(0, HEIGHT - b.h)
            b.dx = randint(-2, 2)
            b.dy = randint(-2, 2)
            if b.dx == 0 and b.dy == 0:
                b.dx = 1
                b.dy = 1
            b.color = rand_color()
            objects.append(b)

    async def start(self, initial):
        pass

    async def animate(self, t):
        frame = dict()

        for obj in self.objects:
            for x in range(obj.x, obj.x + obj.w):
                for y in range(obj.y, obj.y + obj.h):
                    frame[(x, y)] = obj.color
            obj.x += obj.dx
            obj.y += obj.dy
            if obj.x < 0:
                obj.dx *= -1
                obj.x = 0
            elif obj.x >= WIDTH - obj.w:
                obj.dx *= -1
                obj.x = WIDTH - obj.w
            if obj.y < 0:
                obj.dy *= -1
                obj.y = 0
            elif obj.y >= HEIGHT - obj.h:
                obj.dy *= -1
                obj.y = HEIGHT - obj.h

        return frame
