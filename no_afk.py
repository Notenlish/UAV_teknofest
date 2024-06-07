import time

import pyautogui


def dont_be_afk(interval):
    while True:
        # Move the mouse slightly to prevent sleep
        pyautogui.write("Hello world! ", interval=0.25)
        time.sleep(interval)


if __name__ == "__main__":
    # Set the interval in seconds
    interval = 20  # Adjust this as needed
    time.sleep(5)
    dont_be_afk(interval)
