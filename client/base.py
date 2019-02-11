import socket


WIDTH = 15
HEIGHT = 15
LED_TABLE = ('led-table', 1337)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_cmd(channel, command, data):
    length = len(data)
    packet = bytearray([channel, command, length >> 8, length & 0xff])
    packet.extend(data)
    sock.sendto(packet, LED_TABLE)


def send_frame(frame):
    data = bytearray()
    for y in range(15):
        for x in range(15):
            data.extend(bytearray(frame[x][y].tobytes()))
    send_cmd(0, 0, data)


def send_updates(updates):
    data = bytearray()
    for (x, y), color in updates:
        data.extend([x, y])
        data.extend(color.tobytes())

    if data:
        send_cmd(0, 1, data)


def set_pixel_color(x, y, color):
    send_updates([((x, y), color)])


def send_reset():
    send_frame([[Color(0, 0, 0)] * WIDTH] * HEIGHT)


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def tobytes(self):
        return bytearray([self.r, self.g, self.b])

    def __repr__(self):
        return '(%d, %d, %d)' % (self.r, self.g, self.b)
