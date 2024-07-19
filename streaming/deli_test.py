import cv2
import numpy as np
import pygame
import threading
import sys

# Constants
PORT = 12345  # Port used on the server
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Global variables
frame_data = None
frame_lock = threading.Lock()


def receive_ffmpeg_stream(port, use_udp=True):
    global frame_data
    protocol = "udp" if use_udp else "tcp"
    url = f"{protocol}://127.0.0.1:{port}"
    cap: cv2.Mat = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surf = pygame.surfarray.make_surface(frame)

        # Flip the frame for mirroring
        # frame = cv2.flip(frame, 1)
        # # Convert frame to RGB for Pygame compatibility
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Acquire lock to update the global frame_data

        with frame_lock:
            frame_data = surf

    cap.release()


def main():
    global frame_data
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Video Stream Client")

    # Frame rate and clock setup
    clock = pygame.time.Clock()

    # Start the frame receiving thread
    thread = threading.Thread(
        target=receive_ffmpeg_stream, args=(PORT, True), daemon=True
    )
    thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if frame_data is not None:
            try:
                # Resize the frame
                # frame = cv2.resize(frame_data, (WINDOW_WIDTH, WINDOW_HEIGHT))
                # Convert the frame to a Pygame surface
                surface = frame_data
                screen.blit(surface, (0, 0))
                pygame.display.update()

                # Cap the frame rate
                clock.tick(60)  # Adjust the frame rate as necessary
            except Exception as e:
                print(f"Error processing frame: {e}")


if __name__ == "__main__":
    main()
