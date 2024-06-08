# taken from: https://github.com/mandrelbrotset/udp-video-streaming

import cv2
import socket
import math
import pickle
import sys
import os

try:
    from gstream import gstreamer_pipeline
except ModuleNotFoundError:
    from streaming.gstream import gstreamer_pipeline

max_length = 65000
host = "127.0.0.1"  # sys.argv[1]
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if sys.platform == "linux" or sys.platform == "linux2":
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
else:
    cap = cv2.VideoCapture(0)


ret, frame = cap.read()

while ret:
    ret, frame = cap.read()
    # compress frame
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size / max_length)

        frame_info = {"packs": num_of_packs}

        # send the number of packs to be expected
        # print("Number of packs:", num_of_packs)
        sock.sendto(pickle.dumps(frame_info), (host, port))

        left = 0
        right = max_length

        for i in range(num_of_packs):
            # print("left:", left)
            # print("right:", right)

            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length

            # send the frames accordingly
            sock.sendto(data, (host, port))


cap.release()
cv2.destroyAllWindows()

print("done")
