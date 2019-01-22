import numpy as np
import cv2
import socket
import sys

frame = cv2.imread(sys.argv[1])

LED_TABLE = ('led-table', 1338)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# decrease brightness
# https://stackoverflow.com/a/47427398
# value = 25
# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# h, s, v = cv2.split(hsv)

#v[v <= value] = 0
#v[v > value] -= value

#final_hsv = cv2.merge((h, s, v))
#frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

new_frame = cv2.resize(frame, (15, 15))

data = bytearray()
for y in range(15):
    for x in range(15):
        data.extend(bytearray(new_frame[x][y].tobytes()))

sock.sendto(data, LED_TABLE)
