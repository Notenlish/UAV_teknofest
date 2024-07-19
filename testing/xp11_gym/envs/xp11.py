import gymnasium as gym
from gymnasium import spaces
from scipy.spatial import distance
from math import pi, sin, cos
import numpy as np
import pygame
import colorsys


class XPlaneRotationEnvironment(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        self.window_size = np.array([512, 512])  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        print("observation space may be wrong, idk")
        self.observation_space = spaces.Dict(
            {
                # velocity, orientation
                "agent": spaces.Box(
                    low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32
                ),
                "target": spaces.Box(
                    low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32
                ),
            }
        )

        # increase or decrease the yaw, roll, pitch
        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def step(self, action):
        # Apply the action to X-Plane (adjust orientation)
        self.xplane.send_data({"orientation": action})

        # Get the current state
        data = self.xplane.get_all_data()
        position = data["position"]
        velocity = data["velocity"]
        orientation = data["orientation"]

        # Calculate the distance to the target position
        distance = np.linalg.norm(
            np.array(
                [
                    self.target_position[0] - position["local_x"],
                    self.target_position[1] - position["local_y"],
                    self.target_position[2] - position["local_z"],
                ]
            )
        )

        # Define a reward function (e.g., negative distance to the target position)
        reward = -distance

        # Check if the target position is reached
        done = distance < 10  # Example threshold

        # Create the observation array
        observation = np.array(
            [
                position["local_x"],
                position["local_y"],
                position["local_z"],
                velocity["local_vx"],
                velocity["local_vy"],
                velocity["local_vz"],
                orientation["pitch"],
                orientation["roll"],
                orientation["yaw"],
            ]
        )

        return observation, reward, done, {}

    def reset(self):
        # Reset the position of the aircraft to a random position
        # This can be customized as needed
        self.agent = {"vel": np.array([0, 0, 0]), "rot": np.array([0, 0, 0])}
        self.target = {"vel": np.array([0, 0, 0]), "rot": np.array([0, 0, 0])}

        initial_position = [0, 1000, 0, 0, 0, 0]  # Example initial position
        self.xplane.send_data({"position": initial_position})

        # Get the initial state
        data = self.xplane.get_all_data()
        velocity = data["velocity"]
        orientation = data["orientation"]

        observation = np.array(
            [
                velocity["local_vx"],
                velocity["local_vy"],
                velocity["local_vz"],
                orientation["pitch"],
                orientation["roll"],
                orientation["yaw"],
            ]
        )
        return observation

    def render(self):
        if self.render_mode == "human":
            rad = 50
            center = self.window_size / 2
            draw = lambda x, c: pygame.draw.line(
                self.window,
                c,
                center,
                (center + np.array([cos(x) * rad, sin(x) * rad])),
                5,
            )
            i = 0
            values = np.array([self.agent["vel"], self.agent["rot"]]).flatten()
            for x in values:
                c = colorsys.hsv_to_rgb(i / len(values), 0.7, 0.6)
                c = [c[0] * 255, c[1] * 255, c[2] * 255]  # de normalize
                draw(x, c)
                i += len(values)
        pass  # Visualization can be added if needed

    def close(self):
        pass
