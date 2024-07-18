import cv2
import numpy as np
import socket

# Configuration Parameters
UDP_IP_ADDRESS = "0.0.0.0"  # Replace with the IP address of the receiving PC
UDP_PORT = 5000  # Replace with the UDP port you are using for streaming
OUTPUT_FILE = "received_stream.mp4"  # The file where the video will be saved

# Set up the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP_ADDRESS, UDP_PORT))

# Define codec and create VideoWriter object for saving the video
# Video format: MPEG-4 Part 14 (MP4)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_width = 1280  # Set the width of the video frames
frame_height = 720  # Set the height of the video frames
fps = 25  # Set the frames per second

# Create VideoWriter object
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, fps, (frame_width, frame_height))

print(f"Listening for UDP stream on {UDP_IP_ADDRESS}:{UDP_PORT}...")

# Receive and process the video stream
while True:
    # Receive video data from the UDP socket
    data, addr = sock.recvfrom(65535)  # Buffer size can be adjusted as needed
    
    # Convert data to a numpy array
    np_data = np.frombuffer(data, dtype=np.uint8)

    # Create a video capture object from the numpy array
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    if frame is not None:
        # Write the frame to the output file
        out.write(frame)
        
        # Display the frame (optional)
        cv2.imshow('Receiving Video Stream', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("No frame received.")
        
# Release everything if job is finished
sock.close()
out.release()
cv2.destroyAllWindows()

print("Video stream reception finished.")