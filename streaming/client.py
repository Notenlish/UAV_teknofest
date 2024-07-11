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

# Constants
MAX_LENGTH = 65000
HOST = "192.168.1.52"
PORT = 5000

# Set mode: "STREAM" or "RECORD"
MODE = "STREAM"

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Video capture initialization based on the platform
if sys.platform.startswith("linux"):
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
else:
    cap = cv2.VideoCapture(0)

# Ensure the recording directory exists
if MODE == "RECORD" and not os.path.exists("recording"):
    os.makedirs("recording")

# Read the first frame
ret, frame = cap.read()
frame_index = 0

while ret:
    ret, frame = cap.read()
    if not ret:
        break

    # Compress frame to JPEG format
    retval, buffer = cv2.imencode(".jpg", frame)
    if not retval:
        continue

    buffer = buffer.tobytes()
    buffer_size = len(buffer)
    num_of_packs = math.ceil(buffer_size / MAX_LENGTH)

    # Frame information to be sent first
    frame_info = {"packs": num_of_packs}
    sock.sendto(pickle.dumps(frame_info), (HOST, PORT))

    # Send the frame in chunks
    for i in range(num_of_packs):
        start = i * MAX_LENGTH
        end = start + MAX_LENGTH
        data = buffer[start:end]
        sock.sendto(data, (HOST, PORT))

    if MODE == "RECORD":
        # Save the frame to a file
        with open(f"recording/frame_{frame_index:06d}.jpg", "wb") as f:
            f.write(buffer)
        frame_index += 1

# Release resources
cap.release()
cv2.destroyAllWindows()
sock.close()

print("done")
