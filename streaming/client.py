import cv2

def receive_ffmpeg_stream(port, use_udp=True):
    protocol = 'udp' if use_udp else 'tcp'
    url = f'{protocol}://0.0.0.0:{port}'
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    port = 12345  # Should match the port used on the server
    receive_ffmpeg_stream(port, use_udp=True)