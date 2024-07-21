import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

# Define the state transition matrix
dt = 1.0  # time step
F = np.array([[1, dt], [0, 1]])

# Define the observation matrix
H = np.array([[1, 0]])

# Define initial state and covariance matrix
x0 = np.array([[0], [0]])  # initial state (position and velocity)
P0 = np.diag([100, 100])  # initial covariance matrix

# Define process noise covariance matrix Q
Q = Q_discrete_white_noise(dim=2, dt=dt, var=0.1)

# Define measurement noise covariance matrix R
R = np.array([[10]])

# Create Kalman filter
kf = KalmanFilter(dim_x=2, dim_z=1)
kf.F = F
kf.H = H
kf.x = x0
kf.P = P0
kf.Q = Q
kf.R = R

# Simulate projectile motion
true_pos = []
measurements = []
filtered_pos = []

# Simulate motion with constant velocity
num_steps = 50
for t in range(num_steps):
    # True position and velocity
    true_position = 0.5 * 9.8 * t**2  # Assuming g = 9.8 m/s^2
    true_velocity = 9.8 * t

    # Simulate measurement with noise
    measurement = true_position + np.random.randn() * np.sqrt(R[0, 0])

    # Kalman filter prediction and update
    kf.predict()
    kf.update(measurement)

    # Record true position, measurement, and filtered position
    true_pos.append(true_position)
    measurements.append(measurement)
    filtered_pos.append(kf.x[0, 0])

# Plot the results
import matplotlib.pyplot as plt

plt.plot(range(num_steps), true_pos, label="True Position")
plt.plot(range(num_steps), measurements, "ro", label="Measurements")
plt.plot(range(num_steps), filtered_pos, label="Filtered Position")
plt.xlabel("Time Steps")
plt.ylabel("Position (m)")
plt.title("Kalman Filter for Projectile Motion")
plt.legend()
plt.grid(True)
plt.show()
