"""
粒子特效类
"""

import pygame
import random

class Particle:
    """粒子特效类"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = 30
        
    def update(self):
        """更新粒子状态"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size *= 0.95
        
    def draw(self, screen):
        """绘制粒子"""
        alpha = min(255, self.life * 8)
        color_with_alpha = (*self.color, alpha)
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))