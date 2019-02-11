import sys
import socket
import time
from random import randint


from base import WIDTH, HEIGHT, set_pixel_color, Color

BLACK = Color(0, 0, 0)


def rand_color():
    return Color(
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )


while True:
    color = rand_color()
    x = randint(0, WIDTH - 1)
    y = randint(0, HEIGHT - 1)
    set_pixel_color(x, y, color)
    time.sleep(0.02)
