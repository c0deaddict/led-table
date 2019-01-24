import sys
import socket
import time
from random import randint

LED_TABLE = ('led-table', 1338)
WIDTH = 15
HEIGHT = 15

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def to_bytes(self):
        return bytearray([self.r, self.g, self.b])

    def __repr__(self):
        return '(%d, %d, %d)' % (self.r, self.g, self.b)


BLACK = Color(0, 0, 0)


def rand_color():
    return Color(
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    )


def send_image(image):
    data = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            data.extend(image[x][y].to_bytes())

    sock.sendto(data, LED_TABLE)


image = [[BLACK for x in range(WIDTH)] for y in range(HEIGHT)]
while True:
    color = rand_color()
    x = randint(0, WIDTH - 1)
    y = randint(0, HEIGHT - 1)
    image[x][y] = color
    send_image(image)
    time.sleep(0.01)
