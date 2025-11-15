"""
弹弓类
"""

import pygame
import math
from src.utils.constants import *

class Slingshot:
    """弹弓类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self, screen, bird):
        """绘制弹弓"""
        # 弹弓支架
        pygame.draw.rect(screen, DARK_BROWN, (self.x - 8, self.y - 60, 16, 70), 0, 5)
        pygame.draw.rect(screen, DARK_BROWN, (self.x - 28, self.y - 60, 16, 70), 0, 5)
        
        # 弹弓皮筋
        if bird.dragging:
            tension = math.sqrt((bird.x - self.x)**2 + (bird.y - self.y)**2) / 100
            rubber_color = (150, 75, 0) if tension > 0.8 else (101, 67, 33)
            
            pygame.draw.line(screen, rubber_color, (self.x, self.y - 60), (bird.x, bird.y), 4)
            pygame.draw.line(screen, rubber_color, (self.x - 20, self.y - 60), (bird.x, bird.y), 4)
        
        # 弹弓装饰
        pygame.draw.circle(screen, (101, 67, 33), (self.x - 5, self.y - 10), 8)
        pygame.draw.circle(screen, (101, 67, 33), (self.x - 25, self.y - 10), 8)