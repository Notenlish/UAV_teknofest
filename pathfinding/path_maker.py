from pydubins import dubins_shortest_path, dubins_path_sample_many, DubinsPath

from shape import Point

class DubinPoint:
    def __init__(self, x, y, theta) -> None:
        """point that the dubins algorithm uses

        Args:
            x (float): point x
            y (float): point y
            theta (float): between 0 and 2pi
        """
        self.x = x
        self.y = y
        self.theta = theta
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.theta

    def as_dict(self):
        return {"x":self.x,"y":self.y,"theta":self.theta}


# usta https://github.com/AndrewWalker/pydubins/blob/master/dubins/dubins.pyx buna bak

class PathMaker:
    def __init__(self) -> None:
        pass
    def run(self, point0: DubinPoint, point1: DubinPoint, rho: float):
        # rho = turning radius
        
        path = DubinsPath()
        result = dubins_shortest_path(path, point0, point1, rho)

        print(result)
        print(path)

if __name__ == '__main__':
    pathmaker = PathMaker()
    pathmaker.run(DubinPoint(0,0,1), DubinPoint(12,9,0.5),4)