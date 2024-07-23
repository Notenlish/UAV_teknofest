import threading
import ctypes

from streaming.server import start_ffmpeg_streaming


class VideoThread(threading.Thread):
    def __init__(self, name, config):
        threading.Thread.__init__(self)

        self.gcs_ip = config["GCS_IP"]
        self.port = config["VIDEO_PORT"]
        self.use_udp = config["VID_USE_UDP"]

        self.name = name

    def run(self):
        try:
            self.proc = start_ffmpeg_streaming(self.gcs_ip, self.port, self.use_udp)
        finally:
            print("ended vid stream subprocess process")

    def get_id(self):
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop(self):
        self.proc.kill()

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Exception raise failure")
        # ne oluyor bilmiyorum
