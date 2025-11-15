"""
背景类
"""

import pygame
import math  # 添加这行
import random
from src.utils.constants import *

class Background:
    """背景类"""
    def __init__(self):
        self.clouds = []
        self.generate_clouds()
        
    def generate_clouds(self):
        """生成随机云朵"""
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'speed': random.uniform(0.2, 0.5),
                'size': random.uniform(0.8, 1.5)
            })
    
    def draw(self, screen):
        """绘制精美背景"""
        # 天空渐变
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(135 + ratio * 50)
            g = int(206 - ratio * 50)
            b = int(235 - ratio * 30)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # 绘制云朵
        for cloud in self.clouds:
            x, y, size = cloud['x'], cloud['y'], cloud['size']
            pygame.draw.circle(screen, CLOUD_WHITE, (int(x), int(y)), int(25 * size))
            pygame.draw.circle(screen, CLOUD_WHITE, (int(x + 20 * size), int(y - 10 * size)), int(20 * size))
            pygame.draw.circle(screen, CLOUD_WHITE, (int(x + 40 * size), int(y)), int(25 * size))
            pygame.draw.circle(screen, CLOUD_WHITE, (int(x + 20 * size), int(y + 10 * size)), int(18 * size))
        
        # 绘制地面
        pygame.draw.rect(screen, GRASS_GREEN, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
        
        # 草地纹理
        for i in range(20):
            x_pos = i * 50
            pygame.draw.arc(screen, (76, 175, 80), 
                          (x_pos, SCREEN_HEIGHT - 90, 40, 30), 
                          math.pi, 2 * math.pi, 3)
    
    def update(self):
        """更新云朵位置"""
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > SCREEN_WIDTH + 100:
                cloud['x'] = -100