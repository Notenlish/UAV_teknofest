from numpy import array, ndarray


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, shape):
        return Point(shape[0], shape[1])

    def get_tuple(self):
        return (self.x, self.y)

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y


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
        return {"x": self.x, "y": self.y, "theta": self.theta}

    def get_pos(self):
        return (self.x, self.y)

    def get_pos_text(self):
        # add .2f if you want
        return f"({self.x:.0f}, {self.y:.0f})"

    def as_array(self):
        return array([self.x, self.y, self.theta])

    @classmethod
    def from_array(cls, arr: ndarray):
        return cls(arr[0], arr[1], arr[2])


if __name__ == "__main__":
    assert Point(1, 2) == Point.from_tuple((1, 2))
