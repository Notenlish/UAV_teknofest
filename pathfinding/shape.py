class Point:
    def __init__(self, x,y) -> None:
        self.x = x
        self.y = y
    
    @classmethod
    def from_tuple(cls, shape):
        return Point(shape[0],shape[1])
    
    def get_tuple(self):
        return (self.x, self.y)
    
    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y

if __name__ == '__main__':
    assert Point(1,2) == Point.from_tuple((1,2))