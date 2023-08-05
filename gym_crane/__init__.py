from gymnasium.envs.registration import register

register(
    id='CraneWorld-v0',
    entry_point='gym_crane.envs:CraneWorld',
    max_episode_steps=1000,
)