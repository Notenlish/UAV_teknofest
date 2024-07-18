import subprocess
import sys

LINUX = sys.platform.startswith("linux")
MIRROR = True


def start_ffmpeg_streaming(client_ip, port, use_udp=True):
    protocol = "udp" if use_udp else "tcp"
    # fmt:off
    command = [
        'ffmpeg',
        '-f', 'dshow',
        '-rtbufsize', '200MB',
        '-i', 'video=/dev/video0' if LINUX else "video=Integrated Camera",
        '-r', '20',
        '-s', '1280x720',
        '-vf', 'hflip' if MIRROR else "", 
        "-flush_packets", "0",
        "-fflags", "nobuffer", # "+genpts",
        # "-analyzeduration", "0",
        "-tune", "zerolatency",
        # "-bf", "0",  # maybe dont allow this?
        '-vcodec', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'veryfast',
        '-f', 'mpegts',
        f'{protocol}://{client_ip}:{port}'
    ]
    # fmt:on

    print(f"Starting FFmpeg with command: {' '.join(command)}")
    subprocess.run(command)


if __name__ == "__main__":
    client_ip = "127.0.0.1"  # Change to your client IP address
    port = 12345  # Change to the port you want to use
    start_ffmpeg_streaming(client_ip, port, use_udp=False)

# ffmpeg -f dshow -i video="Integrated Camera" -vcodec libx264 -pix_fmt yuv420p -preset veryfast -f mpegts udp://127.0.0.1:12345
# see this for speedup: https://www.reddit.com/r/ffmpeg/comments/ikoohx/ffmpeg_command_for_lowest_latency_possible/?rdt=34741&onetap_auto=true&one_tap=true
