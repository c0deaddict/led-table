import numpy as np
import cv2

from base import send_frame


cap = cv2.VideoCapture(2)
# cap = cv2.VideoCapture('/home/jos/Videos/test.mp4')

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # decrease brightness
    # https://stackoverflow.com/a/47427398
    value = 25
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    v[v <= value] = 0
    v[v > value] -= value

    final_hsv = cv2.merge((h, s, v))
    frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    new_frame = cv2.resize(frame, (15, 15))
    send_frame(new_frame)

    # Our operations on the frame come here
    #gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
