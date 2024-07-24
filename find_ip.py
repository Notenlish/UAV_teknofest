import subprocess
import threading
import io
import logging

logger = logging.Logger("wow ip discoverer")
fh = logging.FileHandler("ip.log")
logger.addHandler(fh)


threads: list[threading.Thread] = []
mem = {}
n_count = 4
msg_timeout_count = round(n_count * 0.75)

t_count = 256

i = 0
can_open_threads = True
while can_open_threads:
    t = threading.Thread(target=lambda: None, name=f"t{i}")
    threads.append(t)
    if i == t_count - 1:
        can_open_threads = False
    i += 1

print(f"N-Count:{n_count} Timeout:{msg_timeout_count} Thread count:{len(threads)}")


def test(ip):
    proc = subprocess.Popen(
        f"ping {ip} -n {n_count}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    # print("I have been started")
    count = 0
    while True:
        count += 1
        raw = proc.stdout.readline()
        if not raw:
            break

        line = raw.strip().decode()
        # print(line)
        if line.startswith("Pinging") or line == "":
            continue
        if line in (
            f"Reply from {ip}: Destination host unreachable.",
            "Request timed out.",
            "PING: transmit failed. General failure.",
            "General failure.",
        ):
            #if count > msg_timeout_count:
            #    break
            continue
        if line.endswith("Destination host unreachable."):
            break
        if line.endswith("Control-C"):
            break
        if line.find(r"(100% loss)"):
            break
        mem[ip] = {"result": "works ig?", "output": line}
        # print("output", line)


def join_threads():
    for t in threads:
        # print(t)
        if t.is_alive():
            t.join()
    if mem != {}:
        logger.log(logging.DEBUG, mem)
    # print(mem)


for v1 in range(192, 255):
    print(f"testing {v1}")
    for v2 in range(168, 255):
        for v3 in range(140, 255):  # 160da kaldım
            print(f"testing {v1}.{v2}.{v3}.x")
            for v4 in range(0, 255):
                i = v1
                ip = f"{v1}.{v2}.{v3}.{v4}"

                thread = threading.Thread(target=test, args=(ip,))
                threads[i] = thread
                thread.start()
            join_threads()
        join_threads()
    join_threads()
