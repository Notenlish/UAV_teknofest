import time

import pyautogui


def move_mouse_periodically(interval):
    c = 0
    while True:
        c += 1
        # Move the mouse slightly to prevent sleep
        pyautogui.write("Hello world! ", interval=0.25)
        time.sleep(interval)


if __name__ == "__main__":
    # Set the interval in seconds
    interval = 20  # Adjust this as needed
    time.sleep(5)
    move_mouse_periodically(interval)
