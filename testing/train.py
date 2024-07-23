import gymnasium as gym

env = gym.make("XPlaneML/rotation", render_mode="human")

obs, info = env.reset()
print(obs)
print(info)

for i in range(1000):
    action = env.action_space.sample()
    print(action)
    print(type(action))

    obs, rewards, done, info = env.step(action)
    # env.render()
    if done:
        obs = env.reset()
    print(i)
