#!/usr/bin/env python3
"""
愤怒的小鸟 - 西瓜乐园
主程序入口文件
"""

import pygame
import sys
from src.game import Game

def main():
    """游戏主函数"""
    print("🎮 愤怒的小鸟 🎮")
    print("=" * 40)
    print("游戏控制说明：")
    print("🖱️  鼠标拖动 - 瞄准和发射")
    print("🎯 R 键 - 重置当前小鸟")
    print("📊 T 键 - 显示/隐藏轨迹预测")
    print("➡️  N 键 - 进入下一关")
    print("🐑 目标 - 消灭所有可爱小羊！")
    print("=" * 40)
    
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()