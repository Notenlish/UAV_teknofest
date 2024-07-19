import xp11_env
import gymnasium as gym

env = gym.make("XPlaneML/rotation", render_mode="human")

obs = env.reset()
print(obs)
