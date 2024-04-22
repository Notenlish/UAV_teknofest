import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

class BaseKalmanFilter:
    def __init__(self, initial: float, rate_of_change: float) -> None:
        self.f = KalmanFilter(dim_x=2, dim_z=1)
        self.f.x = np.array([[initial], [rate_of_change]])  # theta  # theta rate of change
        self.f.F = np.array([[1.0, 1.0], [0.0, 1.0]])
        self.f.H = np.array([[1.0, 0.0]])
        self.f.P *= 1000.0
        self.f.R = 5
        self.f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.01)

    def run(self, measurement):
        z = measurement
        self.f.predict()
        self.f.update(z)

        val = self.f.x[0][0]
        val_rate_of_change = self.f.x[1][0]
        next_val = val + val_rate_of_change
        return next_val


class ThetaKalmanFilter(BaseKalmanFilter):
    def __init__(self, initial_theta: float, theta_rate_of_change: float) -> None:
        super().__init__(initial_theta, theta_rate_of_change)

class VelocityKalmanFilter(BaseKalmanFilter):
    def __init__(self, initial_vel: float, acceleration: float) -> None:
        super().__init__(initial_vel, acceleration)    
