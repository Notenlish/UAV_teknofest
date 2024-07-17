import gymnasium as gym
from gymnasium import spaces
import numpy as np
from stable_baselines3 import PPO
from data import XPlaneDataHandler

class XPlaneEnv(gym.Env):
    def __init__(self, target_position):
        super(XPlaneEnv, self).__init__()
        self.xplane = XPlaneDataHandler()
        self.target_position = target_position

        # Define action and observation space
        # Actions could be changes in pitch, roll, and yaw
        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)

        # Observations include position, velocity, and orientation
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(9,), dtype=np.float32)

    def step(self, action):
        # Apply the action to X-Plane (adjust orientation)
        self.xplane.send_data({"orientation": action})

        # Get the current state
        data = self.xplane.get_all_data()
        position = data["position"]
        velocity = data["velocity"]
        orientation = data["orientation"]

        # Calculate the distance to the target position
        distance = np.linalg.norm(np.array([
            self.target_position[0] - position["local_x"],
            self.target_position[1] - position["local_y"],
            self.target_position[2] - position["local_z"]
        ]))

        # Define a reward function (e.g., negative distance to the target position)
        reward = -distance

        # Check if the target position is reached
        done = distance < 10  # Example threshold

        # Create the observation array
        observation = np.array([
            position["local_x"], position["local_y"], position["local_z"],
            velocity["local_vx"], velocity["local_vy"], velocity["local_vz"],
            orientation["pitch"], orientation["roll"], orientation["yaw"]
        ])

        return observation, reward, done, {}

    def reset(self):
        # Reset the position of the aircraft to a random position
        # This can be customized as needed
        initial_position = [0, 1000, 0, 0, 0, 0]  # Example initial position
        self.xplane.send_data({"position": initial_position})

        # Get the initial state
        data = self.xplane.get_all_data()
        position = data["position"]
        velocity = data["velocity"]
        orientation = data["orientation"]

        observation = np.array([
            position["local_x"], position["local_y"], position["local_z"],
            velocity["local_vx"], velocity["local_vy"], velocity["local_vz"],
            orientation["pitch"], orientation["roll"], orientation["yaw"]
        ])
        return observation

    def render(self, mode='human'):
        pass  # Visualization can be added if needed

    def close(self):
        pass

# Example usage
if __name__ == "__main__":
    # Define the target position
    target_position = [1000, 2000, 1000]  # Example target position

    # Create the environment
    env = XPlaneEnv(target_position)

    # Create the RL model
    model = PPO("MlpPolicy", env, verbose=1)

    # Train the RL model
    model.learn(total_timesteps=10000)

    # Save the trained model
    model.save("ppo_xplane")

    # Load the trained model
    model = PPO.load("ppo_xplane")

    # Run the trained model
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        if done:
            obs = env.reset()
