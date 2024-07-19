import cv2
import pygame
import threading
import numpy as np
import socket
import sys



WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Global variables
global frame_data
frame_data = None
frame_lock = threading.Lock()

class VideoError(Exception):
    pass


class VideoReceive:
    def __init__(self, port, host, use_udp=True) -> None:
        self.port = port
        self.protocol = 'udp' if use_udp else 'tcp'
        self.url = f'{self.protocol}://{host}:{port}'

        if use_udp == False:
            print("Please note that you need to give network access for python in firewall + open up a special inbound port for it in advanced firewall settings")
            print("For TCP to work the connection must already be open(first run receiver then sender)")
            self.url += "/?listen"  # the client needs to specify its listening on tcp

    def _start(self, url:str):
        global frame_data
        print("attempting to connect...")
        cap = cv2.VideoCapture(url)
        print("started capture")
        if not cap.isOpened():
            raise VideoError("My hovercraft is full of eels")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            surf = pygame.surfarray.make_surface(frame)

            with frame_lock:
                frame_data = surf

            # cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

        cap.release()
        cv2.destroyAllWindows()

    def start(self):
        print("starting capture")
        err_count = 0
        while err_count < 10:
            try:
                self._start(self.url)
            except VideoError:
                err_count += 1
            except:
                err_count += 10
                raise Exception("aaaaaaaaaaaaaaaaaaaaa")
            
    def main(self):
            
        global frame_data
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Video Stream Client")

        # Frame rate and clock setup
        clock = pygame.time.Clock()

        # Start the frame receiving thread
        thread = threading.Thread(
            target=self.start, daemon=True
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
    port = 12345  # Should match the port used on the server
    use_udp = False
    host = "127.0.0.1"
    
    receive = VideoReceive(port, host, use_udp=use_udp)
    receive.main()