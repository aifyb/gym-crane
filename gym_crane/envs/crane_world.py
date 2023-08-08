# _*_ coding: utf-8 _*_

from typing import Any
import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
from ..docs import conf


class CraneWorld(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 60}

    def __init__(self, render_mode=None):
        self.window_width = conf.WINDOW_WIDTH
        self.window_height = conf.WINDOW_HEIGHT
        # 轨道上下边界 比例系数
        k = 0.06
        self.track_up = self.window_height / 2- k * self.window_height
        self.track_down = self.window_height / 2+ k * self.window_height

        # 天车高度, 宽度为高度的0.7倍, 任务标识与天车一致
        self.crane_height = 2 * k * self.window_height
        self.crane_width = 0.7*self.crane_height

        # 界面显示字体及字体大小
        pygame.font.init()
        self.font_size = int(0.03*self.window_height)
        self.font = pygame.font.SysFont("Arial", self.font_size)

        self.observation_space = spaces.Dict({
        #     'position': spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32),
        #     'task_start': spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32),
        #     'task_end': spaces.Box(low=0, high=self.window_width, shape=(1,), dtype=np.float32),
            'position': spaces.Discrete(self.window_width),
            'task_start': spaces.Discrete(self.window_width),
            'task_end': spaces.Discrete(self.window_width),
            'load': spaces.Discrete(2), # 0: no load, 1: load
        })

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
            'load': self.load,
        }

    def _get_info(self):
        return {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # self.position = spaces.Box(
        #     low=0, high=self.window_width, shape=(1,), dtype=np.float32).sample()
        # self.task_start = spaces.Box(
        #     low=0, high=self.window_width, shape=(1,), dtype=np.float32).sample()
        # self.task_end = spaces.Box(
        #     low=0, high=self.window_width, shape=(1,), dtype=np.float32).sample()
        self.position = spaces.Discrete(self.window_width).sample()
        self.task_start = spaces.Discrete(self.window_width).sample()
        self.task_end = spaces.Discrete(self.window_width).sample()
        self.load = 0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == 'human':
            self._render_frame()

        return observation, info
    # 判断空载和负载情况
    def _is_load(self):
        if not self.load and self.position == self.task_start:
            self.load = 1
        elif self.load and self.position == self.task_end:
            self.load = 0
        else:
            self.load = self.load

    def step(self, action):
        direction = self._action_to_direction[action]
        self.position += direction
        self._is_load()
        observation = self._get_obs()
        info = self._get_info()

        terminated = np.array_equal(self.position, self.task_end)
        reward = 1 if terminated else 0

        if self.render_mode == 'human':
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == 'human':
            self._render_frame()

    def _render_frame(self):
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height))
            self.clock = pygame.time.Clock()

        self.window.fill((255, 255, 255))

        # track
        pygame.draw.line(self.window, (0, 0, 0), (0, self.track_up),
                         (self.window_width, self.track_up), 3)
        pygame.draw.line(self.window, (0, 0, 0), (0, self.track_down),
                         (self.window_width, self.track_down), 3)
        
        # task
        pygame.draw.rect(self.window, (255, 0, 0), \
            (self.task_start.item(), self.track_up, self.crane_width, self.crane_height), 0)
        pygame.draw.rect(self.window, (0, 255, 0), \
            (self.task_end.item(), self.track_up, self.crane_width, self.crane_height), 0)
        self.window.blit(self.font.render("start", True, "black"), (self.task_start.item(), self.track_up-self.font_size-10))
        self.window.blit(self.font.render("end", True, "black"), (self.task_end.item(), self.track_up-self.font_size-10))
        
        # crane
        if self.load:
            pygame.draw.rect(self.window, (0, 0, 255), \
                (self.position.item(), self.track_up, self.crane_width, self.crane_height), 0)
        else:
            pygame.draw.rect(self.window, (0, 0, 0), \
                (self.position.item(), self.track_up, self.crane_width, self.crane_height), 0)

        pygame.display.flip()
        self.clock.tick(self.metadata['render_fps'])


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None