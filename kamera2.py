import subprocess
import threading
import random

quality = 30  # 0 - 100(highest quality)

v = random.randint(0, 1000)
filename = f"output-{v}.mp4"

gst_args = (
    "gst-launch-1.0",
    "nvarguscamerasrc",
    "!",
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=20/1, format=NV12",
    "!",
    "nvvidconv",
    "!",
    "video/x-raw, format=I420",
    "!",
    "videoconvert",
    "!",
    "filesink",
    "location=/dev/stdout",
    "sync=false",
)


ffmpeg_args = (
    "ffmpeg",
    "-f",
    "rawvideo",
    "-pix_fmt",
    "yuv420p",
    "-s",
    "1280x720",
    "-r",
    "20",
    "-i",
    "-",
    "-c:v",
    "libx264",
    "-preset",
    "veryfast",
    "-crf",
    f"{quality}",
    filename,
)


def run_gstreamer():
    proc = subprocess.Popen(gst_args, stdout=subprocess.PIPE, bufsize=10**8)
    return proc


def run_ffmpeg(pipe):
    proc2 = subprocess.Popen(ffmpeg_args, stdin=pipe)
    proc2.wait()


print(filename)

gst_proc = run_gstreamer()
ffmpeg_thread = threading.Thread(target=run_ffmpeg, args=(gst_proc.stdout,))

try:
    ffmpeg_thread.start()
    gst_proc.wait()
    ffmpeg_thread.join()
except KeyboardInterrupt:
    gst_proc.terminate()
    ffmpeg_thread.join()
