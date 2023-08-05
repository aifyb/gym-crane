from gymnasium.envs.registration import register

register(
    id='CarneWorld-v0',
    entry_point='gym_crane.envs:CarneWorld',
    max_episode_steps=1000,
)