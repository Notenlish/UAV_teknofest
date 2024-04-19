class Camera:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x, self.y)
    
    def move(self, dirx,diry, dt):
        self.x += dirx * 100 * (dt / 1000)
        self.y += diry * 100 * (dt / 1000)