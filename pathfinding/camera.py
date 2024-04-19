class Camera:
    def __init__(self, x=0, y=0, speed=150) -> None:
        self.x = x
        self.y = y
        self.speed = speed

    def get_pos(self):
        return (self.x, self.y)
    
    def move(self, dirx,diry, dt):
        time_passed_s = dt / 1000
        self.x += dirx * self.speed * time_passed_s
        self.y += diry * self.speed * time_passed_s