try:
    from testing.xpc import XPlaneConnect
except ModuleNotFoundError:
    from xpc import XPlaneConnect


class Testing:
    def __init__(self) -> None:
        self.xp = XPlaneConnect(port=50501, timeout=10000)
        self.xp.sendPOSI([37.6219, -122.3421, 2500, 0, 0, 0, 0])


if __name__ == "__main__":
    testing = Testing()
