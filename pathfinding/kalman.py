import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from shape import DubinPoint


class UAVKalmanFilter:
    def __init__(
        self,
        target_dub_pos: DubinPoint,
        measurement_noise_variance,
        process_noise_variance,
    ):
        """
        Initialize the Kalman Filter for the UAV.

        Parameters:
        - measurement_noise_variance: Variance of the measurement noise.
        - process_noise_variance: Variance of the process noise.
        """
        # Initialize the Kalman Filter
        self.kf = KalmanFilter(
            dim_x=3, dim_z=3
        )  # Updated to include theta in the measurements

        # Measurement matrix (H)
        self.kf.H = np.array(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        )  # Updated to include theta

        # Initial state
        self.kf.x = target_dub_pos.as_array()  # [x, y, theta]

        # Initial covariance matrix
        self.kf.P *= 1000  # Start with a large uncertainty

        # Measurement noise covariance
        self.kf.R = np.array(
            [
                [measurement_noise_variance, 0, 0],
                [0, measurement_noise_variance, 0],
                [0, 0, measurement_noise_variance],
            ]
        )  # Updated to include theta

        # Process noise covariance will be updated dynamically
        self.process_noise_variance = process_noise_variance  ### I added this...

    def update_state_transition_matrix(self, dt, velocity):
        """
        Update the state transition matrix based on the current velocity and time step.

        Parameters:
        - dt: Time step between frames.
        - velocity: Current velocity of the UAV.
        """
        # State transition matrix (A)
        # Assuming the UAV moves in a straight line with constant velocity and changes angle theta
        # The state vector is [x, y, theta]
        self.kf.F = np.array([[1, 0, -dt * velocity], [0, 1, 0], [0, 0, 1]])

        # Process noise covariance (Q)
        # Assuming no control input affects the state directly
        self.kf.Q = Q_discrete_white_noise(
            dim=3, dt=dt, var=self.process_noise_variance
        )  ## not sure if it is correct

    def predict(self):
        """
        Predict the next state of the UAV.
        """
        self.kf.predict()
        return self.kf.x

    def update(self, measurement: DubinPoint):
        """
        Update the prediction with the actual measurement.

        Parameters:
        - measurement: The actual measurement of the UAV's position and angle.
        """
        self.kf.update(measurement.as_array())
        return self.kf.x

    def _run(self, dt, velocity, measurement: DubinPoint):
        # i dont think this would work
        self.update_state_transition_matrix(dt, velocity)

        predicted_state = self.predict()

        updated_state = uav_kalman_filter.update(measurement.as_array())
        return predicted_state, updated_state


if __name__ == "__main__":
    # Initialize the Kalman Filter
    measurement_noise_variance = 0.1  # Example value
    process_noise_variance = 0.01  # Example value
    uav_kalman_filter = UAVKalmanFilter(
        DubinPoint(0, 0, 0), measurement_noise_variance, process_noise_variance
    )

    # Update state transition matrix and process noise covariance matrix
    dt = 0.1  # Time step between frames
    velocity = 1.0  # Current velocity of the UAV
    uav_kalman_filter.update_state_transition_matrix(dt, velocity)

    # Predict the next state
    predicted_state = uav_kalman_filter.predict()

    # Update with the actual measurement including theta
    actual_measurement = np.array([10, 20, 0.5])  # Example measurement including theta
    updated_state = uav_kalman_filter.update(actual_measurement)
    print(updated_state)
