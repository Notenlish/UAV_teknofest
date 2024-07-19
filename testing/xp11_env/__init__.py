from gymnasium.envs.registration import register

register(
    id="XPlaneML/rotation",
    entry_point="xp11_env.envs:XPlaneEnv",
)
