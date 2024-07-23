import cv2

# Camera properties
fps = 30.0
frame_width = 1920
frame_height = 1080

# GStreamer pipeline to send camera output as TCP
ip = "127.0.0.1"  # Replace with the target IP address
port = 12945       # Replace with the target port
gst_str = f"appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host={ip} port={port} sync=false"

# Create OpenCV VideoCapture object
cap = cv2.VideoCapture(0)



cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

# Create OpenCV VideoWriter object with GStreamer pipeline
out = cv2.VideoWriter(gst_str, cv2.CAP_GSTREAMER, 0, fps, (frame_width, frame_height), True)

if not cap.isOpened():
    print("Error: Unable to open the camera")
    exit()
if not out.isOpened():
    print("Error: Unable to open the GStreamer pipeline")
    exit()

print("Streaming camera output to", ip, "on port", port)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from the camera")
        break
    
    # Write the frame to the GStreamer pipeline
    out.write(frame)
    
    # Display the frame (optional)
    cv2.imshow('Camera', frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# B
# https://forums.developer.nvidia.com/t/gstreamer-tcpserversink-2-3-seconds-latency/183388/4
# https://forums.developer.nvidia.com/t/video-streaming/246362

# $ gst-launch-1.0 videotestsrc is-live=1 ! video/x-raw,width=1280,height=720 ! timeoverlay valignment=4 halignment=1 ! nvvidconv ! 'video/x-raw(memory:NVMM),width=1280,height=720' ! tee name=t ! nvv4l2h264enc insert-sps-pps=1 idrinterval=15 ! h264parse ! rtph264pay ! udpsink host=10.19.106.10 port=5000 sync=0 t. ! queue ! nvegltransform ! nveglglessink sync=0
