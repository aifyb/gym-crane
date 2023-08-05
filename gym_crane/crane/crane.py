# -*- coding: utf-8 -*-
import random

class Crane:
    def __init__(self, position, direction='left', speed=1):
        self.position = position
        self.direction = direction
        self.speed = speed

    def get_status(self):
        return self.position, self.direction, self.speed
    
    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == 'left' and self.position > 0:
            self.position -= self.speed
        elif self.direction == 'right' and self.position < 1280:
            self.position += self.speed
        else:
            self.position = self.position


