import numpy as np

class KalmanFilter:
    def __init__(self, initial_state, initial_covariance, process_variance, measurement_variance):
        self.x = initial_state  # Initial state estimate (position)
        self.P = initial_covariance  # Initial covariance matrix
        self.Q = process_variance  # Process noise covariance
        self.R = measurement_variance  # Measurement noise covariance

    def predict(self, A):
        # Prediction step
        # A: State transition matrix (e.g., [1, dt; 0, 1] for constant velocity)
        self.x = np.dot(A, self.x)
        self.P = np.dot(np.dot(A, self.P), A.T) + self.Q

    def update(self, z, H):
        # Update step
        # z: Measurement (e.g., position from sensor)
        # H: Measurement matrix (e.g., [1, 0] for position measurement)
        y = z - np.dot(H, self.x)
        S = np.dot(np.dot(H, self.P), H.T) + self.R
        K = np.dot(np.dot(self.P, H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(np.dot(K, H), self.P)

# Example usage:
initial_state = np.array([[0], [0]])  # Initial position and velocity
initial_covariance = np.array([[1000, 0], [0, 1000]])  # Initial covariance matrix
process_variance = 1e-5  # Process noise variance
measurement_variance = 0.1**2  # Measurement noise variance

kf = KalmanFilter(initial_state, initial_covariance, process_variance, measurement_variance)

# Assuming you have a measurement z (e.g., from a sensor)
z = np.random.normal(0, 0.1)  # Simulated noisy measurement
H = np.array([[1, 0]])  # Measurement matrix (position measurement)

kf.predict(A=np.array([[1, 1], [0, 1]]))  # Example state transition matrix
kf.update(z, H)

# Estimated position after prediction and update:
estimated_position = kf.x[0, 0]
print(f"Estimated position: {estimated_position:.2f}")
