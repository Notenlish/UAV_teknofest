import gymnasium as gym
from gymnasium import spaces
from scipy.spatial import distance
from math import pi, sin, cos
import numpy as np
import pygame
import colorsys

import time

from data import XPlaneDataHandler


class XPlaneEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None):
        self.xplane = XPlaneDataHandler()
        self.window_size = np.array([512, 512])  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        print("observation space may be wrong, idk")
        self.observation_space = spaces.Dict(
            {
                # velocity, rotation
                "agent": spaces.Box(
                    low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32
                ),
                "target": spaces.Box(
                    low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32
                ),
            }
        )

        # increase or decrease the yaw, roll, pitch
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)

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

        self.start_time = time.time()

    def reset(self):
        start_pos = [130_000, 3_000, 130_000]
        self.xplane.send_data({"position": start_pos})

        # Reset the position of the aircraft to a random position
        # This can be customized as needed
        self.agent = {
            "velocity": np.array([0, 0, 0], dtype=np.float32),
            "rotation": np.array([0, 0, 0], dtype=np.float32),
        }
        self.target = {
            "velocity": np.array([0, 0, 0], dtype=np.float32),
            "rotation": np.array([0, 0, 0], dtype=np.float32),
        }

        # initial_position = [0, 1000, 0, 0, 0, 0]  # Example initial position
        # self.xplane.send_data({"position": initial_position})

        # Get the initial state
        self.get_values()

        observation = {"agent": self.agent, "target": self.target}
        info = self._get_info()
        return observation, info

    def get_values(self):
        t_dif = time.time() - self.start_time
        if t_dif < 0.1:
            time.sleep(0.1 - t_dif)
        self.xplane.fetch_drefs()

        self.agent["velocity"] = np.array(list(self.xplane.get_velocity().values()))
        self.agent["rotation"] = np.array(list(self.xplane.get_rotation().values()))

    def _get_info(self):
        return {}

    def _get_rot_diff(self):
        rotation = self.agent["rotation"]
        target_rotation = self.target["rotation"]

        return np.linalg.norm(
            np.array(
                [
                    rotation[0] - target_rotation[0],
                    rotation[1] - target_rotation[1],
                    rotation[2] - target_rotation[2],
                ]
            )
        )

    def step(self, action: np.ndarray):
        # Get the initial state
        self.get_values()

        rot = self.target["rotation"]

        action *= 10

        # Apply the action to X-Plane (adjust rotation)
        self.xplane.send_data({"rot_acc": action})

        observation = {"agent": self.agent, "target": self.target}
        info = self._get_info()

        distance = self._get_rot_diff()
        reward = -distance

        done = False  # TODO: fix this

        return observation, reward, done, {}

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
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
