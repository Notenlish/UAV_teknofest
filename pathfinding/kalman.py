import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise


f = KalmanFilter(dim_x=2, dim_z=1)
f.x = np.array([[0.0], [0.0]])  # position  # velocity
f.F = np.array([[1.0, 1.0], [0.0, 1.0]])
f.H = np.array([[1.0, 0.0]])
f.P *= 1000.0
f.R = 5
f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.01)


def get_measurement(v):
    return v + 1


def run(measurement, f: KalmanFilter):
    print(f"measurement {measurement} pos: {f.x[0][0]:.2f} vel: {f.x[1][0]:.2f}")
    print(f"Prediction in next step: {f.x[0][0] + f.x[1][0]:.2f}")


for v in range(10):
    z = get_measurement(v)
    f.predict()
    f.update(z)
    run(z, f)
