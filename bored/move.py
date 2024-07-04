import pyautogui
import time
WIDTH, HEIGHT = pyautogui.size()
import math


# gotta make it just add commands to a list for an async class to run

class Mover:
    def __init__(self) -> None:
        pass
    
    def move(self, x, y):
        # x and y is -1 - 1
        center = centerx, centery = (960, 436)
        half_w = 99
        half_h = 99
        
        x = centerx + round(half_w * x)
        y = centery + round(half_h * y)
        
        pyautogui.moveTo(x, y, duration=0.001)
    
    def set_throttle(self, v):
        if v == -1:
            pyautogui.keyDown("f1")
            pyautogui.keyUp("f2")
        if v == 0:
            pyautogui.keyUp("f1")
            pyautogui.keyUp("f2")
        if v == 1:
            pyautogui.keyUp("f1")
            pyautogui.keyDown("f2")
    
    def full_power(self):
        self.set_throttle(1)
        time.sleep(5)
    
    def take_off(self):
        self.full_power()
        
        pyautogui.press("B", _pause=0.1)
        time.sleep(0.01)
        i = 0
        while i <= 200:
            if i <= 170:
                self.set_throttle(1)
                y = i / 300
                self.move(y / 10, y)
            else:
                self.move(1, 0)
            i += 1
            print(i)
        self.move(0,0)

    def follow_uav(self, result):
        wanted_size = (round(WIDTH * 0.3),round(WIDTH * 0.3))
        w_diff = result.w - wanted_size[0]
        h_diff = result.h - wanted_size[1]
        
        # normalized diff
        n_w_diff = self.cam_res[0] / w_diff
        n_h_diff = self.cam_res[1] / h_diff
        
        base_speed = 0.5
        speed = base_speed + (n_w_diff / 2)
        self.set_throttle(speed)
        
        center = [result.x, result.y]
        sc_center = [self.cam_res[0]//2, self.cam_res[1]]
        
        pos_diff_x = center[0] - sc_center[0]
        pos_diff_y = center[1] - sc_center[1]

        n_pos_difx = self.cam_res[0] / pos_diff_x  # -1  -  1
        n_pos_dify = self.cam_res[1] / pos_diff_y  # -1  -  1

        roll_rad = math.radians(n_pos_difx * 90)
        pitch_rad = math.radians(n_pos_dify * 90)  # gotta test this out

        self.set_roll(roll_rad)
        self.set_pitch(pitch_rad)

if __name__ == '__main__':
    m = Mover()
    time.sleep(3)
    m.take_off()