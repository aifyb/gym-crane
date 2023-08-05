from typing import Any
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np


class CarneWorld(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 5}

    def __init__(self, render_mode=None):
        # Define window size
        self.window_width = 800
        self.window_height = 600

        self.observation_space = spaces.Dict({
            'position': spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32),
            'task_start': spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32),
            'task_end': spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32),
        })
        print(self.observation_space)

        self.action_space = spaces.Discrete(3)

        self._action_to_direction = {
            0: 0,           # stay
            1: -1,          # left
            2: 1,           # right
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):
        return {
            'position': self.position,
            'task_start': self.task_start,
            'task_end': self.task_end,
        }
    
    def _get_info(self):
        return {}
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.position = spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32).sample()
        self.task_start = spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32).sample()
        self.task_end = spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32).sample()

        observation = self._get_obs()
        print(observation)
        info = self._get_info()

        if self.render_mode == 'human':
            self._render_frame()

        return observation, info
    

    def step(self, action):
        direction = self._action_to_direction[action]
        self.position += direction
        print(self.position)

        observation = self._get_obs()
        info = self._get_info()

        terminated = np.array_equal(self.position, self.task_end)
        reward = 1 if terminated else 0 

        if self.render_mode == 'human':
            self._render_frame()

        return observation, reward, terminated, False, info
    
    def render(self):
        if self.render_mode == 'human':
            mode = self._render_frame()

    def _render_frame(self):
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
            self.clock = pygame.time.Clock()

        self.window.fill((255, 255, 255))


        # 中心位置绘制单轨行车道
        pygame.draw.line(self.window, (0, 0, 0), (0, self.window_height/2-35), (self.window_width, self.window_height/2-35), 3)
        pygame.draw.line(self.window, (0, 0, 0), (0, self.window_height/2+35), (self.window_width, self.window_height/2+35), 3)

        # 根据task_start 绘制任务起点
        pygame.draw.line(self.window, (255, 0, 0), (self.task_start.item(), self.window_height/2-35), (self.task_start.item(), self.window_height/2+35), 3)
        # 根据task_end 绘制任务终点
        pygame.draw.line(self.window, (0, 255, 0), (self.task_end.item(), self.window_height/2-35), (self.task_end.item(), self.window_height/2+35), 3)
        # 根据position 绘制行车位置
        pygame.draw.line(self.window, (0, 0, 0), (self.position.item(), self.window_height/2-35), (self.position.item(), self.window_height/2+35), 3)

        pygame.display.flip()
        self.clock.tick(self.metadata['render_fps'])

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None