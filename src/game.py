"""
游戏主类
"""

import pygame
import sys
import math
import os
import random

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from entities.bird import Bird
    from entities.sheep import Sheep
    from entities.watermelon import Watermelon
    from entities.slingshot import Slingshot
    from environment.background import Background
    from utils.constants import *
except ImportError:
    # 如果直接运行 game.py，使用相对导入
    from .entities.bird import Bird
    from .entities.sheep import Sheep
    from .entities.watermelon import Watermelon
    from .entities.slingshot import Slingshot
    from .environment.background import Background
    from .utils.constants import *

class Game:
    """游戏主类"""
    def __init__(self):
        # 先初始化 pygame
        pygame.init()
        
        # 然后创建屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎯 愤怒的小鸟 - 西瓜乐园 🐦")
        self.clock = pygame.time.Clock()
        
        # 设置窗口图标
        self._set_window_icon()
        
        # 初始化音效
        self._init_sounds()
        
        # 现在初始化字体（在 pygame.init() 之后）
        self._init_fonts()
        
        # 创建游戏对象
        slingshot_x = 200
        slingshot_y = 550
        self.background = Background()
        self.slingshot = Slingshot(slingshot_x, slingshot_y)
        self.sheeps = []
        self.watermelons = []
        
        # 小鸟管理
        self.birds = []  # 改为小鸟列表
        self.current_bird_index = 0
        self.bird_colors = [RED, BLUE, GREEN, PURPLE, ORANGE]  # 不同颜色的小鸟
        self.max_birds = 500  # 每关最多500只小鸟
        
        # 游戏状态
        self.score = 0
        self.level = 1
        self.game_over = False
        self.level_complete = False
        self.show_trajectory = False
        self.sound_enabled = True
        
        # 初始化关卡
        self.setup_level()
    
    def _set_window_icon(self):
        """设置窗口图标 - 支持 ICO 和 PNG 格式"""
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # 图标文件的可能路径（优先查找您放的 images 文件夹）
        icon_paths = [
            # 您选择的位置 - assets/images/favicon.ico
            os.path.join(project_root, 'assets', 'images', 'favicon.ico'),
            
            # 其他可能的位置
            os.path.join(project_root, 'favicon.ico'),
            os.path.join(project_root, 'assets', 'favicon.ico'),
            os.path.join(project_root, 'assets', 'images', 'icon.png'),
            os.path.join(project_root, 'icon.png'),
        ]
        
        print("🔍 正在查找图标文件...")
        icon_loaded = False
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    # 加载图标
                    icon = pygame.image.load(icon_path)
                    # 设置窗口图标
                    pygame.display.set_icon(icon)
                    print(f"✅ 成功加载应用图标: {os.path.basename(icon_path)}")
                    print(f"📁 图标路径: {icon_path}")
                    icon_loaded = True
                    break
                except Exception as e:
                    print(f"❌ 加载图标失败 {icon_path}: {e}")
            else:
                print(f"🔍 未找到: {icon_path}")
        
        if not icon_loaded:
            print("⚠️ 未找到可用的图标文件，将使用默认Pygame图标")
    
    def _init_fonts(self):
        """初始化字体"""
        # 确保字体模块已初始化
        if not pygame.font.get_init():
            pygame.font.init()
        
        # 字体文件路径
        fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts')
        font_path = os.path.join(fonts_dir, 'wqy-microhei-lite.ttc')
        
        print(f"查找字体文件: {font_path}")
        print(f"字体文件存在: {os.path.exists(font_path)}")
        
        # 尝试加载文泉驿微米黑字体
        if os.path.exists(font_path):
            try:
                self.title_font = pygame.font.Font(font_path, 48)
                self.ui_font = pygame.font.Font(font_path, 28)
                self.small_font = pygame.font.Font(font_path, 20)
                self.signature_font = pygame.font.Font(font_path, 16)
                
                # 测试字体是否能正常渲染中文
                test_text = self.title_font.render("测试", True, WHITE)
                print("✅ 成功加载文泉驿微米黑字体，中文支持正常")
                
            except Exception as e:
                print(f"❌ 加载文泉驿字体失败: {e}")
                print("使用默认字体")
                self._load_default_fonts()
        else:
            print(f"❌ 字体文件未找到: {font_path}")
            print("使用默认字体")
            self._load_default_fonts()
    
    def _load_default_fonts(self):
        """加载默认字体"""
        self.title_font = pygame.font.Font(None, 48)
        self.ui_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.signature_font = pygame.font.Font(None, 16)
    
    def _init_sounds(self):
        """初始化音效"""
        self.sounds = {}
        sounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds')
        
        # 音效文件列表 - 使用您提供的文件名
        sound_files = {
            'bg_music': 'angry_bird.mp3'  # 使用您的背景音乐文件
        }
        
        # 尝试加载每个音效
        for sound_name, filename in sound_files.items():
            file_path = os.path.join(sounds_dir, filename)
            if os.path.exists(file_path):
                try:
                    if sound_name == 'bg_music':
                        # 背景音乐特殊处理
                        self.sounds[sound_name] = file_path
                        print(f"✅ 加载背景音乐: {filename}")
                    else:
                        self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                        print(f"✅ 加载音效: {filename}")
                except Exception as e:
                    print(f"❌ 加载音效失败 {filename}: {e}")
                    self.sounds[sound_name] = None
            else:
                print(f"⚠️ 音效文件未找到: {filename}")
                self.sounds[sound_name] = None
        
        # 播放背景音乐
        self._play_background_music()
    
    def _play_background_music(self):
        """播放背景音乐"""
        if 'bg_music' in self.sounds and self.sounds['bg_music']:
            try:
                pygame.mixer.music.load(self.sounds['bg_music'])
                pygame.mixer.music.set_volume(0.5)  # 设置音量
                pygame.mixer.music.play(-1)  # -1 表示循环播放
                print("🎵 背景音乐开始播放")
            except Exception as e:
                print(f"❌ 播放背景音乐失败: {e}")
    
    def play_sound(self, sound_name):
        """播放指定音效"""
        if self.sound_enabled and sound_name in self.sounds and self.sounds[sound_name] is not None:
            try:
                if sound_name == 'bg_music':
                    # 背景音乐已经在播放
                    pass
                else:
                    self.sounds[sound_name].play()
            except:
                pass
    
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.music.unpause()
            print("🔊 音效已开启")
        else:
            pygame.mixer.music.pause()
            print("🔇 音效已关闭")
        return self.sound_enabled
    
    def setup_level(self):
        """设置关卡 - 第一关7组，第二关8组，第三关9组，第四关10组"""
        self.sheeps = []
        self.watermelons = []
        
        # 创建小鸟队列
        self.birds = []
        self.current_bird_index = 0
        for i in range(self.max_birds):
            bird = Bird(200, 550)
            bird.color = self.bird_colors[i % len(self.bird_colors)]  # 分配不同颜色
            self.birds.append(bird)
        
        if self.level == 1:
            # 第一关：7组简单的羊和西瓜
            # 第一组（右下角）
            self.sheeps.extend([
                Sheep(750, 580),
                Sheep(780, 550),
                Sheep(720, 550)
            ])
            self.watermelons.extend([
                Watermelon(700, 530),
                Watermelon(740, 530)
            ])
            
            # 第二组（中间偏右）
            self.sheeps.extend([
                Sheep(600, 500),
                Sheep(630, 470),
                Sheep(570, 470)
            ])
            self.watermelons.extend([
                Watermelon(550, 450),
                Watermelon(590, 450)
            ])
            
            # 第三组（右上角 - 第一组）
            self.sheeps.extend([
                Sheep(850, 450),
                Sheep(880, 420),
                Sheep(820, 420)
            ])
            self.watermelons.extend([
                Watermelon(800, 400),
                Watermelon(840, 400)
            ])
            
            # 第四组（中间偏上）
            self.sheeps.extend([
                Sheep(500, 400),
                Sheep(530, 370),
                Sheep(470, 370)
            ])
            self.watermelons.extend([
                Watermelon(450, 350),
                Watermelon(490, 350)
            ])
            
            # 第五组（左上角）
            self.sheeps.extend([
                Sheep(650, 350),
                Sheep(680, 320),
                Sheep(620, 320)
            ])
            self.watermelons.extend([
                Watermelon(600, 300),
                Watermelon(640, 300)
            ])
            
            # 第六组（右上角 - 第二组，更高位置）
            self.sheeps.extend([
                Sheep(920, 380),
                Sheep(950, 350),
                Sheep(890, 350)
            ])
            self.watermelons.extend([
                Watermelon(870, 330),
                Watermelon(910, 330)
            ])
            
            # 第七组（右上角 - 第三组，最高位置）
            self.sheeps.extend([
                Sheep(980, 320),
                Sheep(1010, 290),
                Sheep(950, 290)
            ])
            self.watermelons.extend([
                Watermelon(930, 270),
                Watermelon(970, 270)
            ])
            
        elif self.level == 2:
            # 第二关：8组中等难度的羊和西瓜
            # 第一组（底部右侧）
            self.sheeps.extend([
                Sheep(800, 580),
                Sheep(780, 530),
                Sheep(820, 530),
                Sheep(800, 480)
            ])
            self.watermelons.extend([
                Watermelon(720, 530),
                Watermelon(760, 530),
                Watermelon(740, 480)
            ])
            
            # 第二组（中间右侧）
            self.sheeps.extend([
                Sheep(650, 500),
                Sheep(680, 470),
                Sheep(620, 470),
                Sheep(650, 420)
            ])
            self.watermelons.extend([
                Watermelon(600, 470),
                Watermelon(640, 470),
                Watermelon(620, 420)
            ])
            
            # 第三组（右上角 - 第一组）
            self.sheeps.extend([
                Sheep(900, 450),
                Sheep(930, 420),
                Sheep(870, 420),
                Sheep(900, 370)
            ])
            self.watermelons.extend([
                Watermelon(850, 420),
                Watermelon(890, 420),
                Watermelon(870, 370)
            ])
            
            # 第四组（中间左侧）
            self.sheeps.extend([
                Sheep(550, 400),
                Sheep(580, 370),
                Sheep(520, 370),
                Sheep(550, 320)
            ])
            self.watermelons.extend([
                Watermelon(500, 370),
                Watermelon(540, 370),
                Watermelon(520, 320)
            ])
            
            # 第五组（顶部左侧）
            self.sheeps.extend([
                Sheep(700, 350),
                Sheep(730, 320),
                Sheep(670, 320),
                Sheep(700, 270)
            ])
            self.watermelons.extend([
                Watermelon(650, 320),
                Watermelon(690, 320),
                Watermelon(670, 270)
            ])
            
            # 第六组（右上角 - 第二组，更高位置）
            self.sheeps.extend([
                Sheep(950, 380),
                Sheep(980, 350),
                Sheep(920, 350),
                Sheep(950, 300)
            ])
            self.watermelons.extend([
                Watermelon(900, 350),
                Watermelon(940, 350),
                Watermelon(920, 300)
            ])
            
            # 第七组（右上角 - 第三组，最高位置）
            self.sheeps.extend([
                Sheep(1020, 320),
                Sheep(1050, 290),
                Sheep(990, 290),
                Sheep(1020, 240)
            ])
            self.watermelons.extend([
                Watermelon(970, 290),
                Watermelon(1010, 290),
                Watermelon(990, 240)
            ])
            
            # 第八组（新增 - 左侧高空）
            self.sheeps.extend([
                Sheep(350, 350),
                Sheep(380, 320),
                Sheep(320, 320),
                Sheep(350, 290)
            ])
            self.watermelons.extend([
                Watermelon(300, 320),
                Watermelon(340, 320),
                Watermelon(320, 290)
            ])
            
        elif self.level == 3:
            # 第三关：9组复杂的羊和西瓜
            # 第一组（大型结构 - 右下角）
            self.sheeps.extend([
                Sheep(850, 580),
                Sheep(830, 530),
                Sheep(870, 530),
                Sheep(850, 480),
                Sheep(830, 430)
            ])
            self.watermelons.extend([
                Watermelon(750, 530),
                Watermelon(790, 530),
                Watermelon(770, 480),
                Watermelon(810, 480),
                Watermelon(790, 430)
            ])
            
            # 第二组（塔形结构 - 中间）
            self.sheeps.extend([
                Sheep(600, 550),
                Sheep(600, 500),
                Sheep(600, 450),
                Sheep(570, 500),
                Sheep(630, 500)
            ])
            self.watermelons.extend([
                Watermelon(550, 530),
                Watermelon(590, 530),
                Watermelon(570, 480),
                Watermelon(610, 480),
                Watermelon(590, 430)
            ])
            
            # 第三组（分散结构 - 右上角第一组）
            self.sheeps.extend([
                Sheep(950, 550),
                Sheep(920, 500),
                Sheep(980, 500),
                Sheep(950, 450),
                Sheep(920, 400),
                Sheep(980, 400)
            ])
            self.watermelons.extend([
                Watermelon(900, 530),
                Watermelon(940, 530),
                Watermelon(920, 480),
                Watermelon(960, 480),
                Watermelon(940, 430),
                Watermelon(980, 430)
            ])
            
            # 第四组（线性结构 - 左上角）
            self.sheeps.extend([
                Sheep(450, 500),
                Sheep(480, 470),
                Sheep(420, 470),
                Sheep(450, 420),
                Sheep(480, 390),
                Sheep(420, 390)
            ])
            self.watermelons.extend([
                Watermelon(400, 470),
                Watermelon(440, 470),
                Watermelon(420, 420),
                Watermelon(460, 420),
                Watermelon(440, 370)
            ])
            
            # 第五组（金字塔结构 - 中间顶部）
            self.sheeps.extend([
                Sheep(750, 350),
                Sheep(720, 320),
                Sheep(780, 320),
                Sheep(690, 290),
                Sheep(750, 290),
                Sheep(810, 290),
                Sheep(720, 260),
                Sheep(780, 260)
            ])
            self.watermelons.extend([
                Watermelon(700, 320),
                Watermelon(740, 320),
                Watermelon(780, 320),
                Watermelon(720, 290),
                Watermelon(760, 290),
                Watermelon(740, 260)
            ])
            
            # 第六组（右上角 - 第二组，城堡结构）
            self.sheeps.extend([
                Sheep(1020, 480),
                Sheep(1050, 450),
                Sheep(990, 450),
                Sheep(1020, 420),
                Sheep(1050, 390),
                Sheep(990, 390),
                Sheep(1020, 360)
            ])
            self.watermelons.extend([
                Watermelon(970, 450),
                Watermelon(1010, 450),
                Watermelon(990, 420),
                Watermelon(1030, 420),
                Watermelon(1010, 390),
                Watermelon(1050, 390)
            ])
            
            # 第七组（右上角 - 第三组，高空平台）
            self.sheeps.extend([
                Sheep(1080, 350),
                Sheep(1110, 320),
                Sheep(1050, 320),
                Sheep(1080, 290),
                Sheep(1110, 260),
                Sheep(1050, 260),
                Sheep(1080, 230),
                Sheep(1110, 200)
            ])
            self.watermelons.extend([
                Watermelon(1030, 320),
                Watermelon(1070, 320),
                Watermelon(1050, 290),
                Watermelon(1090, 290),
                Watermelon(1070, 260),
                Watermelon(1110, 260),
                Watermelon(1090, 230)
            ])
            
            # 第八组（左侧高空塔）
            self.sheeps.extend([
                Sheep(350, 350),
                Sheep(380, 320),
                Sheep(320, 320),
                Sheep(350, 290),
                Sheep(380, 260),
                Sheep(320, 260)
            ])
            self.watermelons.extend([
                Watermelon(300, 320),
                Watermelon(340, 320),
                Watermelon(320, 290),
                Watermelon(360, 290),
                Watermelon(340, 260)
            ])
            
            # 第九组（中间高空结构）
            self.sheeps.extend([
                Sheep(680, 280),
                Sheep(710, 250),
                Sheep(650, 250),
                Sheep(680, 220),
                Sheep(710, 190),
                Sheep(650, 190),
                Sheep(680, 160)
            ])
            self.watermelons.extend([
                Watermelon(630, 250),
                Watermelon(670, 250),
                Watermelon(650, 220),
                Watermelon(690, 220),
                Watermelon(670, 190),
                Watermelon(710, 190)
            ])
            
        elif self.level == 4:
            # 第四关：10组终极挑战
            # 第一组（超级塔 - 右下角）
            self.sheeps.extend([
                Sheep(850, 580),
                Sheep(830, 530),
                Sheep(870, 530),
                Sheep(850, 480),
                Sheep(830, 430),
                Sheep(870, 430),
                Sheep(850, 380)
            ])
            self.watermelons.extend([
                Watermelon(750, 530),
                Watermelon(790, 530),
                Watermelon(770, 480),
                Watermelon(810, 480),
                Watermelon(790, 430),
                Watermelon(830, 430),
                Watermelon(810, 380)
            ])
            
            # 第二组（大型金字塔 - 中间右侧）
            self.sheeps.extend([
                Sheep(600, 550),
                Sheep(570, 500),
                Sheep(630, 500),
                Sheep(540, 450),
                Sheep(600, 450),
                Sheep(660, 450),
                Sheep(570, 400),
                Sheep(630, 400)
            ])
            self.watermelons.extend([
                Watermelon(550, 530),
                Watermelon(590, 530),
                Watermelon(570, 480),
                Watermelon(610, 480),
                Watermelon(590, 430),
                Watermelon(630, 430),
                Watermelon(610, 380)
            ])
            
            # 第三组（城堡结构 - 右上角）
            self.sheeps.extend([
                Sheep(950, 550),
                Sheep(920, 500),
                Sheep(980, 500),
                Sheep(950, 450),
                Sheep(920, 400),
                Sheep(980, 400),
                Sheep(950, 350),
                Sheep(920, 300),
                Sheep(980, 300)
            ])
            self.watermelons.extend([
                Watermelon(900, 530),
                Watermelon(940, 530),
                Watermelon(920, 480),
                Watermelon(960, 480),
                Watermelon(940, 430),
                Watermelon(980, 430),
                Watermelon(960, 380),
                Watermelon(1000, 380)
            ])
            
            # 第四组（复杂结构 - 左上角）
            self.sheeps.extend([
                Sheep(450, 500),
                Sheep(480, 470),
                Sheep(420, 470),
                Sheep(450, 420),
                Sheep(480, 390),
                Sheep(420, 390),
                Sheep(450, 340),
                Sheep(480, 310),
                Sheep(420, 310)
            ])
            self.watermelons.extend([
                Watermelon(400, 470),
                Watermelon(440, 470),
                Watermelon(420, 420),
                Watermelon(460, 420),
                Watermelon(440, 370),
                Watermelon(480, 370),
                Watermelon(460, 320)
            ])
            
            # 第五组（巨型金字塔 - 中间顶部）
            self.sheeps.extend([
                Sheep(750, 350),
                Sheep(720, 320),
                Sheep(780, 320),
                Sheep(690, 290),
                Sheep(750, 290),
                Sheep(810, 290),
                Sheep(660, 260),
                Sheep(720, 260),
                Sheep(780, 260),
                Sheep(840, 260),
                Sheep(690, 230),
                Sheep(750, 230),
                Sheep(810, 230)
            ])
            self.watermelons.extend([
                Watermelon(700, 320),
                Watermelon(740, 320),
                Watermelon(780, 320),
                Watermelon(720, 290),
                Watermelon(760, 290),
                Watermelon(800, 290),
                Watermelon(740, 260),
                Watermelon(780, 260),
                Watermelon(760, 230)
            ])
            
            # 第六组（高空城堡 - 右上角）
            self.sheeps.extend([
                Sheep(1020, 480),
                Sheep(1050, 450),
                Sheep(990, 450),
                Sheep(1020, 420),
                Sheep(1050, 390),
                Sheep(990, 390),
                Sheep(1020, 360),
                Sheep(1050, 330),
                Sheep(990, 330),
                Sheep(1020, 300)
            ])
            self.watermelons.extend([
                Watermelon(970, 450),
                Watermelon(1010, 450),
                Watermelon(990, 420),
                Watermelon(1030, 420),
                Watermelon(1010, 390),
                Watermelon(1050, 390),
                Watermelon(1030, 360),
                Watermelon(1070, 360)
            ])
            
            # 第七组（超高空平台）
            self.sheeps.extend([
                Sheep(1080, 350),
                Sheep(1110, 320),
                Sheep(1050, 320),
                Sheep(1080, 290),
                Sheep(1110, 260),
                Sheep(1050, 260),
                Sheep(1080, 230),
                Sheep(1110, 200),
                Sheep(1050, 200),
                Sheep(1080, 170)
            ])
            self.watermelons.extend([
                Watermelon(1030, 320),
                Watermelon(1070, 320),
                Watermelon(1050, 290),
                Watermelon(1090, 290),
                Watermelon(1070, 260),
                Watermelon(1110, 260),
                Watermelon(1090, 230),
                Watermelon(1130, 230),
                Watermelon(1110, 200)
            ])
            
            # 第八组（左侧超级塔）
            self.sheeps.extend([
                Sheep(350, 350),
                Sheep(380, 320),
                Sheep(320, 320),
                Sheep(350, 290),
                Sheep(380, 260),
                Sheep(320, 260),
                Sheep(350, 230),
                Sheep(380, 200),
                Sheep(320, 200)
            ])
            self.watermelons.extend([
                Watermelon(300, 320),
                Watermelon(340, 320),
                Watermelon(320, 290),
                Watermelon(360, 290),
                Watermelon(340, 260),
                Watermelon(380, 260),
                Watermelon(360, 230),
                Watermelon(400, 230)
            ])
            
            # 第九组（中间高空复杂结构）
            self.sheeps.extend([
                Sheep(680, 280),
                Sheep(710, 250),
                Sheep(650, 250),
                Sheep(680, 220),
                Sheep(710, 190),
                Sheep(650, 190),
                Sheep(680, 160),
                Sheep(710, 130),
                Sheep(650, 130)
            ])
            self.watermelons.extend([
                Watermelon(630, 250),
                Watermelon(670, 250),
                Watermelon(650, 220),
                Watermelon(690, 220),
                Watermelon(670, 190),
                Watermelon(710, 190),
                Watermelon(690, 160),
                Watermelon(730, 160)
            ])
            
            # 第十组（终极挑战 - 最高点）
            self.sheeps.extend([
                Sheep(900, 180),
                Sheep(930, 150),
                Sheep(870, 150),
                Sheep(900, 120),
                Sheep(930, 90),
                Sheep(870, 90),
                Sheep(900, 60)
            ])
            self.watermelons.extend([
                Watermelon(850, 150),
                Watermelon(890, 150),
                Watermelon(870, 120),
                Watermelon(910, 120),
                Watermelon(890, 90),
                Watermelon(930, 90),
                Watermelon(910, 60)
            ])
    
    def get_current_bird(self):
        """获取当前活跃的小鸟"""
        if self.current_bird_index < len(self.birds):
            return self.birds[self.current_bird_index]
        return None
    
    def next_bird(self):
        """切换到下一只小鸟"""
        self.current_bird_index += 1
        if self.current_bird_index >= len(self.birds):
            # 所有小鸟都用完了
            return False
        return True
    
    def draw_ui(self):
        """绘制UI"""
        panel = pygame.Surface((300, 120), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 128))
        self.screen.blit(panel, (10, 10))
        
        score_text = self.ui_font.render(f"🏆 分数: {self.score}", True, WHITE)
        level_text = self.ui_font.render(f"🎯 关卡: {self.level}/4", True, WHITE)
        birds_text = self.ui_font.render(f"🐦 剩余小鸟: {len(self.birds) - self.current_bird_index}", True, WHITE)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(level_text, (20, 50))
        self.screen.blit(birds_text, (20, 80))
        
        current_bird = self.get_current_bird()
        if current_bird and not current_bird.launched and not current_bird.dragging:
            hint_text = self.small_font.render("拖动小鸟来发射！", True, WHITE)
            self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, 100))
        
        if current_bird and current_bird.dragging:
            power = math.sqrt((current_bird.start_x - current_bird.x)**2 + (current_bird.start_y - current_bird.y)**2)
            power_bar_width = min(200, power * 2)
            pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH // 2 - 100, 80, power_bar_width, 15), 0, 7)
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH // 2 - 100, 80, 200, 15), 2, 7)
            
            power_text = self.small_font.render("发射力量", True, WHITE)
            self.screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, 60))
    
    def draw_signature(self):
        """绘制署名"""
        signature_text = self.signature_font.render("@2025 Designed by Pengchao Ma", True, (200, 200, 200))
        
        # 计算居中位置（底部）
        text_x = SCREEN_WIDTH // 2 - signature_text.get_width() // 2  # 水平居中
        text_y = SCREEN_HEIGHT - signature_text.get_height() - 20    # 距离底部20像素
        
        signature_bg = pygame.Surface((signature_text.get_width() + 10, signature_text.get_height() + 6), pygame.SRCALPHA)
        signature_bg.fill((0, 0, 0, 128))
        self.screen.blit(signature_bg, (text_x - 5, text_y - 3))
        
        self.screen.blit(signature_text, (text_x, text_y))
    
    def draw_trajectory(self):
        """绘制发射轨迹预测"""
        current_bird = self.get_current_bird()
        if current_bird and current_bird.dragging and not current_bird.launched:
            power_x = current_bird.start_x - current_bird.x
            power_y = current_bird.start_y - current_bird.y
            
            points = []
            vx = power_x * LAUNCH_POWER
            vy = power_y * LAUNCH_POWER
            px, py = current_bird.x, current_bird.y
            
            for _ in range(50):
                vy += GRAVITY
                px += vx
                py += vy
                points.append((px, py))
                
                if px < 0 or px > SCREEN_WIDTH or py > SCREEN_HEIGHT:
                    break
            
            if len(points) > 1:
                pygame.draw.lines(self.screen, (255, 255, 255, 128), False, points, 2)
                
                for i, point in enumerate(points):
                    if i % 5 == 0:
                        alpha = 255 - i * 5
                        if alpha > 0:
                            surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                            pygame.draw.circle(surf, (255, 255, 255, alpha), (3, 3), 3)
                            self.screen.blit(surf, (point[0] - 3, point[1] - 3))
    
    def handle_events(self):
        """处理游戏事件"""
        current_bird = self.get_current_bird()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_bird and not current_bird.launched and not current_bird.dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    distance = math.sqrt((mouse_x - current_bird.x) ** 2 + (mouse_y - current_bird.y) ** 2)
                    if distance < current_bird.radius:
                        current_bird.dragging = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if current_bird and current_bird.dragging:
                    current_bird.dragging = False
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    power_x = current_bird.start_x - mouse_x
                    power_y = current_bird.start_y - mouse_y
                    current_bird.launch(power_x, power_y)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if current_bird:
                        current_bird.reset()
                elif event.key == pygame.K_t:
                    self.show_trajectory = not self.show_trajectory
                elif event.key == pygame.K_n and self.level_complete:
                    self.level += 1
                    if self.level > 4:
                        self.game_over = True
                    else:
                        self.setup_level()
                        self.level_complete = False
                elif event.key == pygame.K_m:  # M键切换音效
                    sound_status = "开启" if self.toggle_sound() else "关闭"
                    print(f"音效{sound_status}")
        
        if current_bird and current_bird.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = current_bird.start_x - mouse_x
            dy = current_bird.start_y - mouse_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > MAX_PULL_DISTANCE:
                scale = MAX_PULL_DISTANCE / distance
                dx *= scale
                dy *= scale
            
            current_bird.x = current_bird.start_x - dx
            current_bird.y = current_bird.start_y - dy
        
        return True
    
    def update(self):
        """更新游戏状态"""
        self.background.update()
        
        current_bird = self.get_current_bird()
        if not current_bird:
            return
        
        # 更新所有小鸟
        for bird in self.birds:
            bird.update()
        
        # 如果当前小鸟已经发射且不再活跃，切换到下一只
        if current_bird.launched and not current_bird.active:
            if not self.next_bird():
                # 所有小鸟都用完了，检查关卡是否完成
                alive_sheeps = [sheep for sheep in self.sheeps if sheep.alive]
                if not alive_sheeps and not self.level_complete:
                    self.level_complete = True
                    self.score += 500 * self.level
                elif alive_sheeps and not self.level_complete:
                    # 所有小鸟用完但还有羊存活，游戏结束
                    self.game_over = True
        
        # 检测碰撞（只检测当前活跃的小鸟）
        if current_bird.active:
            for sheep in self.sheeps[:]:
                if sheep.alive and current_bird.check_collision(sheep):
                    sheep.hit()
                    self.score += 100
            
            # 西瓜碰撞
            for watermelon in self.watermelons:
                if watermelon.check_collision(current_bird):
                    watermelon.crack()
                    current_bird.velocity_x *= -0.3
                    current_bird.velocity_y *= -0.3
        
        # 检查关卡是否完成（所有羊都被消灭）
        alive_sheeps = [sheep for sheep in self.sheeps if sheep.alive]
        if not alive_sheeps and not self.level_complete:
            self.level_complete = True
            self.score += 500 * self.level
    
    def draw(self):
        """绘制游戏画面"""
        self.background.draw(self.screen)
        
        if self.show_trajectory:
            self.draw_trajectory()
        
        # 绘制西瓜
        for watermelon in self.watermelons:
            watermelon.draw(self.screen)
        
        for sheep in self.sheeps:
            sheep.draw(self.screen)
        
        # 绘制所有小鸟
        for bird in self.birds:
            bird.draw(self.screen)
        
        # 绘制弹弓（只与当前小鸟交互）
        current_bird = self.get_current_bird()
        if current_bird:
            self.slingshot.draw(self.screen, current_bird)
        
        self.draw_ui()
        self.draw_signature()
        
        if self.level_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            if self.level < 4:
                complete_text = self.title_font.render(f"关卡 {self.level} 完成！", True, YELLOW)
                next_text = self.ui_font.render("按 N 进入下一关", True, WHITE)
            else:
                complete_text = self.title_font.render("游戏通关！", True, YELLOW)
                next_text = self.ui_font.render("恭喜你完成了所有关卡！", True, WHITE)
            
            self.screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(next_text, (SCREEN_WIDTH // 2 - next_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.title_font.render("游戏结束！", True, RED)
            score_text = self.ui_font.render(f"最终分数: {self.score}", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# 添加直接运行的代码
if __name__ == "__main__":
    print("🎮 愤怒的小鸟 - 西瓜乐园 🎮")
    print("=" * 50)
    print("游戏控制说明：")
    print("🖱️  鼠标拖动 - 瞄准和发射")
    print("🎯 R 键 - 重置当前小鸟")
    print("📊 T 键 - 显示/隐藏轨迹预测")
    print("🎵 M 键 - 开启/关闭音效")
    print("➡️  N 键 - 进入下一关")
    print("🐦 每关有5只不同颜色的小鸟")
    print("🐑 目标 - 消灭所有可爱小羊！")
    print("=" * 50)
    
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)