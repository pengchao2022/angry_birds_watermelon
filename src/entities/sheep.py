"""
小羊类
"""

import pygame
import math
import random
from src.entities.particle import Particle
from src.utils.constants import *

class Sheep:
    """小羊类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = SHEEP_RADIUS
        self.body_color = random.choice(SHEEP_COLORS)
        self.face_color = SHEEP_WHITE
        self.alive = True
        self.hit_particles = []
        self.has_bow = random.choice([True, False])
        self.bow_color = random.choice([RED, BLUE, PURPLE, ORANGE])
        self.has_spot = random.choice([True, False])
        self.spot_color = random.choice([YELLOW, PINK, LIGHT_BLUE])
        
    def draw(self, screen):
        """绘制生动可爱的小羊"""
        if not self.alive:
            return
            
        # 主体 - 毛茸茸的效果
        pygame.draw.circle(screen, self.body_color, (int(self.x), int(self.y)), self.radius)
        
        # 毛茸茸的纹理
        for i in range(12):
            angle = i * math.pi / 6
            distance = self.radius - random.randint(2, 5)
            fluff_x = self.x + math.cos(angle) * distance
            fluff_y = self.y + math.sin(angle) * distance
            fluff_size = random.randint(4, 7)
            pygame.draw.circle(screen, self.body_color, (int(fluff_x), int(fluff_y)), fluff_size)
        
        # 斑点装饰
        if self.has_spot:
            for i in range(2):
                spot_x = self.x + random.randint(-15, 15)
                spot_y = self.y + random.randint(-10, 10)
                pygame.draw.circle(screen, self.spot_color, (int(spot_x), int(spot_y)), 8)
        
        # 脸部
        face_radius = self.radius * 0.6
        pygame.draw.circle(screen, self.face_color, (int(self.x), int(self.y)), int(face_radius))
        
        # 眼睛
        eye_y = self.y - 3
        left_eye_x = self.x - 8
        right_eye_x = self.x + 8
        
        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(eye_y)), 6)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(eye_y)), 6)
        pygame.draw.circle(screen, BLUE, (int(left_eye_x), int(eye_y)), 4)
        pygame.draw.circle(screen, BLUE, (int(right_eye_x), int(eye_y)), 4)
        pygame.draw.circle(screen, BLACK, (int(left_eye_x), int(eye_y)), 2)
        pygame.draw.circle(screen, BLACK, (int(right_eye_x), int(eye_y)), 2)
        pygame.draw.circle(screen, WHITE, (int(left_eye_x - 1), int(eye_y - 1)), 1)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x - 1), int(eye_y - 1)), 1)
        
        # 睫毛
        pygame.draw.line(screen, BLACK, (left_eye_x - 6, eye_y - 4), (left_eye_x - 8, eye_y - 6), 2)
        pygame.draw.line(screen, BLACK, (left_eye_x - 6, eye_y - 2), (left_eye_x - 8, eye_y - 2), 2)
        pygame.draw.line(screen, BLACK, (right_eye_x + 6, eye_y - 4), (right_eye_x + 8, eye_y - 6), 2)
        pygame.draw.line(screen, BLACK, (right_eye_x + 6, eye_y - 2), (right_eye_x + 8, eye_y - 2), 2)
        
        # 嘴巴
        mouth_y = self.y + 5
        pygame.draw.arc(screen, PINK, (self.x - 6, mouth_y - 2, 12, 8), 0.2, math.pi - 0.2, 2)
        
        # 腮红
        blush_y = self.y + 2
        pygame.draw.circle(screen, (255, 200, 200), (int(self.x - 10), int(blush_y)), 4)
        pygame.draw.circle(screen, (255, 200, 200), (int(self.x + 10), int(blush_y)), 4)
        
        # 耳朵
        ear_color = (min(255, self.body_color[0] + 30), 
                    min(255, self.body_color[1] + 30), 
                    min(255, self.body_color[2] + 30))
        
        pygame.draw.ellipse(screen, ear_color, (self.x - 22, self.y - 20, 10, 14))
        pygame.draw.ellipse(screen, (255, 220, 220), (self.x - 20, self.y - 18, 6, 8))
        pygame.draw.ellipse(screen, ear_color, (self.x + 12, self.y - 20, 10, 14))
        pygame.draw.ellipse(screen, (255, 220, 220), (self.x + 14, self.y - 18, 6, 8))
        
        # 蝴蝶结装饰
        if self.has_bow:
            bow_x = self.x
            bow_y = self.y - self.radius - 5
            pygame.draw.circle(screen, self.bow_color, (int(bow_x), int(bow_y)), 5)
            pygame.draw.ellipse(screen, self.bow_color, (bow_x - 8, bow_y - 4, 6, 8))
            pygame.draw.ellipse(screen, self.bow_color, (bow_x + 2, bow_y - 4, 6, 8))
            pygame.draw.rect(screen, self.bow_color, (bow_x - 2, bow_y + 3, 4, 8))
        
        # 绘制击中特效
        for particle in self.hit_particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.life <= 0:
                self.hit_particles.remove(particle)
    
    def hit(self):
        """小羊被击中"""
        self.alive = False
        for _ in range(25):
            color = random.choice([self.body_color, self.spot_color if self.has_spot else self.body_color, 
                                 WHITE, YELLOW, PINK])
            self.hit_particles.append(Particle(self.x, self.y, color))