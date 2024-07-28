import subprocess
import threading
import random

quality = 30  # 0 - 100(highest quality)

gst_args = (
    "gst-launch-1.0",
    "nvarguscamerasrc", "!",
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=20/1, format=NV12", "!",
    "nvjpegenc", f"quality={quality}", "!",
    "image/jpeg, framerate=20/1", "!",
    "filesink", "location=/dev/stdout"
)

v = random.randint(0, 1000)
filename = f"output-{v}.mp4"

ffmpeg_args = (
    "ffmpeg", "-f", "image2pipe", "-framerate", "20", "-vcodec", "mjpeg",
    "-i", "-", "-r", "20", "-vcodec", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", "-f", "mp4", filename
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
