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


def set_pixel_color(x, y, color):
    data = bytearray([x, y])
    data.extend(color.to_bytes())
    send_cmd(0, 1, data)
