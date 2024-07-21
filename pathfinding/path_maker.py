import json

from pydubins import DubinsPath, dubins_path_sample_many, dubins_shortest_path
from shape import DubinPoint, Point

from uav import OwnUAV, TargetUAV

# usta https://github.com/AndrewWalker/pydubins/blob/master/dubins/dubins.pyx buna bak


class PathMaker:
    def __init__(self) -> None:
        pass

    def run(self, own_uav: OwnUAV, target_uav: TargetUAV, rho: float, step_size=0.1):
        # rho = turning radius

        path = DubinsPath()
        _ = dubins_shortest_path(
            path, own_uav.as_dubin_point(), target_uav.as_dubin_point(), rho
        )

        results = {}

        def sample_callback(q, x, user_data):
            results[x] = {"q": [q[0], q[1], q[2]], "user_data": user_data}
            return 0

        _ = dubins_path_sample_many(
            path, stepSize=step_size, cb=sample_callback, user_data={}
        )
        return path, results


if __name__ == "__main__":
    pathmaker = PathMaker()
    path, results = pathmaker.run(DubinPoint(50, 25, 1), DubinPoint(450, 309, 2), 4)
    with open("result.json", "w") as f:
        json.dump(results, f)
