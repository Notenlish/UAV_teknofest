import cv2


class VideoError(Exception):
    pass


class VideoReceive:
    def __init__(self, port, host, use_udp=True) -> None:
        self.protocol = 'udp' if use_udp else 'tcp'
        self.url = f'{self.protocol}://{host}:{port}'

        if use_udp == False:
            print("Please note that you need to give network access for python in firewall + open up a special inbound & outbound port for it in advanced firewall settings")
            print("For TCP to work the connection must already be open(first run receiver then sender)")
            self.url += "/?listen"  # the client needs to specify its listening on tcp

    def _start(self, url:str):
        print("attempting to connect...")
        cap = cv2.VideoCapture(url)
        print("started capture")
        if not cap.isOpened():
            raise VideoError("My hovercraft is full of eels")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow('Video Stream', frame)
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

if __name__ == "__main__":
    port = 12345  # Should match the port used on the server
    use_udp = False
    host = "127.0.0.1"
    
    receive = VideoReceive(port, host, use_udp=use_udp)
    receive.start()
