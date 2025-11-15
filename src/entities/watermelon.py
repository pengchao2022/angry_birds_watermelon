"""
西瓜类
"""

import pygame
import math
import random
from src.entities.particle import Particle
from src.utils.constants import *

class Watermelon:
    """西瓜类"""
    def __init__(self, x, y, size=1.0):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.size = size
        self.crack_particles = []
        self.is_cut = random.choice([True, False])
        
    def draw(self, screen):
        """绘制生动的西瓜"""
        if self.is_cut:
            self._draw_cut_watermelon(screen)
        else:
            self._draw_whole_watermelon(screen)
        
        # 绘制裂纹特效
        for particle in self.crack_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.life <= 0:
                self.crack_particles.remove(particle)
    
    def _draw_whole_watermelon(self, screen):
        """绘制整个西瓜"""
        # 西瓜主体
        pygame.draw.ellipse(screen, WATERMELON_GREEN, (self.x, self.y, self.width, self.height))
        
        # 西瓜条纹
        stripe_width = 4
        for i in range(5):
            stripe_y = self.y + i * (self.height // 4)
            pygame.draw.line(screen, WATERMELON_DARK_GREEN, 
                           (self.x, stripe_y), 
                           (self.x + self.width, stripe_y), stripe_width)
        
        # 西瓜藤
        pygame.draw.line(screen, (139, 69, 19), 
                       (self.x + self.width // 2, self.y - 10),
                       (self.x + self.width // 2, self.y), 3)
        
        # 西瓜叶
        leaf_points = [
            (self.x + self.width // 2, self.y - 10),
            (self.x + self.width // 2 - 8, self.y - 15),
            (self.x + self.width // 2 + 8, self.y - 15)
        ]
        pygame.draw.polygon(screen, (34, 139, 34), leaf_points)
    
    def _draw_cut_watermelon(self, screen):
        """绘制切开的西瓜"""
        # 西瓜果肉
        pygame.draw.ellipse(screen, WATERMELON_RED, (self.x, self.y, self.width, self.height // 2))
        
        # 西瓜皮
        pygame.draw.arc(screen, WATERMELON_GREEN, 
                      (self.x, self.y, self.width, self.height), 
                      math.pi, 2 * math.pi, 8)
        
        # 西瓜籽
        seed_positions = [
            (self.x + 15, self.y + 15),
            (self.x + 45, self.y + 20),
            (self.x + 25, self.y + 25),
            (self.x + 35, self.y + 10)
        ]
        for seed_x, seed_y in seed_positions:
            pygame.draw.ellipse(screen, BLACK, (seed_x, seed_y, 4, 6))
        
        # 果肉纹理
        for i in range(3):
            y_pos = self.y + 5 + i * 8
            pygame.draw.arc(screen, WATERMELON_PINK, 
                          (self.x + 5, y_pos, self.width - 10, 10),
                          0, math.pi, 1)
    
    def crack(self):
        """西瓜破裂特效"""
        for _ in range(15):
            color = random.choice([WATERMELON_RED, WATERMELON_GREEN, WATERMELON_PINK])
            self.crack_particles.append(Particle(
                self.x + random.randint(0, self.width),
                self.y + random.randint(0, self.height),
                color
            ))
    
    def check_collision(self, bird):
        """检测与小鸟的碰撞"""
        if (bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width and
            bird.y + bird.radius > self.y and bird.y - bird.radius < self.y + self.height):
            return True
        return False