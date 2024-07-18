import subprocess
import sys

LINUX = sys.platform.startswith("linux")


def start_ffmpeg_streaming(client_ip, port, use_udp=True):
    protocol = "udp" if use_udp else "tcp"
    # fmt:off
    command = [
        'ffmpeg',
        '-f', 'dshow',
        '-i', 'video=/dev/video0' if LINUX else "video=Integrated Camera",
        '-r', '20',
        '-s', '1280x720',
        "-flush_packets", "0",
        "-fflags", "nobuffer", # "+genpts",
        "-analyzeduration", "0",
        "-tune", "zerolatency",
        "-bf", "0",  # maybe dont allow this?
        '-vcodec', 'libx265',
        '-pix_fmt', 'yuv420p',
        '-preset', 'veryfast',
        '-f', 'mpegts',
        f'{protocol}://{client_ip}:{port}'
    ]
    # fmt:on

    print(f"Starting FFmpeg with command: {' '.join(command)}")
    subprocess.run(command)


if __name__ == "__main__":
    client_ip = "192.168.1.97"  # Change to your client IP address
    port = 12345  # Change to the port you want to use
    start_ffmpeg_streaming(client_ip, port, use_udp=True)

# ffmpeg -f dshow -i video="Integrated Camera" -vcodec libx264 -pix_fmt yuv420p -preset veryfast -f mpegts udp://127.0.0.1:12345
