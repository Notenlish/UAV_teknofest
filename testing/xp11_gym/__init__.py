from gymnasium.envs.registration import register

register(
    id="XPlaneML/rotation",
    entry_point="rl.envs:XPlaneRotationEnvironment",
)
