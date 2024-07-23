import threading
import time


def t():
    time.sleep(2)
    print("4")

t1 = threading.Thread(target=t)
t1.start()
print(t1.is_alive())
t1.join()
print(t1.is_alive())