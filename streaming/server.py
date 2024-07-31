import subprocess
import sys
import socket
import time

LINUX = sys.platform.startswith("linux")
SCHOOL_PC = False
MIRROR = False
win_cam = "video=Integrated Camera" if SCHOOL_PC else "video=HD Webcam"


def start_ffmpeg_streaming(client_ip, port, use_udp=True):
    protocol = "udp" if use_udp else "tcp"
    if not use_udp:
        print(
            "Please note that you need to give network access for python in firewall + open up a special inbound & outbound port for it in advanced firewall settings"
        )
        print(
            "For TCP to work the connection must already be open(first run receiver then sender)"
        )

    # fmt:off
    if not LINUX:
        command = [
        'ffmpeg',
        '-f', 'dshow',
        '-rtbufsize', '200MB',
        '-i', 'video=/dev/video0' if LINUX else win_cam,
        '-r', '20',
        '-s', '1280x720',
        "-flush_packets", "0",
        "-fflags", "nobuffer", # "+genpts",
        # "-analyzeduration", "0",
        "-tune", "zerolatency",
        # "-bf", "0",  # maybe dont allow this?
        '-vcodec', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'veryfast',
        '-f', 'mpegts',
    ]
    if LINUX:
        from kamera import run
        run()
        # get frame data
        while True:
            pass
    if MIRROR:
        command.append('-vf')
        command.append('hflip')
    command.append(f'{protocol}://{client_ip}:{port}')
    # fmt:on

    # print(f"Starting FFmpeg with command: {' '.join(command)}")
    print("starting ffmpeg.")
    print("Terminal output disabled for ffmpeg vid stream")
    return subprocess.Popen(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


# For UBI Range Test(UAV)
def range_test_streaming(client_ip, port, use_udp=True):
    import numpy as np
    from utils import read_config

    try:
        config = read_config("../config.json")
    except FileNotFoundError:
        config = read_config("config.json")

    SEED = config["RANGE_TEST_SEED"]
    MSG_SIZE = config["MSG_SIZE"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        addr = (client_ip, port)
        print(f"connecting UBI test with {addr[0]}:{addr[1]}")
        s.connect(addr)

        while True:
            np.random.seed(SEED)
            u8_max = 2**8
            buf = np.array(
                [round(np.random.random() * u8_max) for _ in range(MSG_SIZE)],
                dtype=np.uint8,
            )

            # Send the data
            s.sendall(buf.tobytes())

            # Receive data
            data = s.recv(MSG_SIZE)  # we wont do anything with it
            # print(f"Received data {data[:10]}...")


if __name__ == "__main__":
    client_ip = "127.0.0.1"
    port = 12345
    range_test_streaming(client_ip, port, use_udp=False)

# ffmpeg -f dshow -i video="Integrated Camera" -vcodec libx264 -pix_fmt yuv420p -preset veryfast -f mpegts udp://127.0.0.1:12345
# see this for speedup: https://www.reddit.com/r/ffmpeg/comments/ikoohx/ffmpeg_command_for_lowest_latency_possible/?rdt=34741&onetap_auto=true&one_tap=true
