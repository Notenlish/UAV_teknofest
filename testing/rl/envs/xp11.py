import gymnasium as gym
from gymnasium import spaces
from scipy.spatial import distance
from math import pi


class XPlaneRotationEnvironment(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    def __init__(self, render_mode=None):
        self.window_size = 512  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        print("observation space may be wrong, idk")
        self.observation_space = spaces.Dict(
            {
                "agent_roll": spaces.Box(-pi, pi, shape=(1), dtype=float),
                "agent_yaw": spaces.Box(-pi, pi, shape=(1), dtype=float),
                "agent_pitch": spaces.Box(-pi, pi, shape=(1), dtype=float),
                "target_roll": spaces.Box(-pi, pi, shape=(1), dtype=float),
                "target_roll": spaces.Box(-pi, pi, shape=(1), dtype=float),
                "target_roll": spaces.Box(-pi, pi, shape=(1), dtype=float),
            }
        )

        # increase or decrease the yaw, roll, pitch
        self.action_space = spaces.Discrete(6)

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
