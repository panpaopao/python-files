import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""                       # screen参数指定飞船要绘制在什么地方
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人飞船并获取其外接矩形
        self.image = pygame.image.load('images/waixingren.bmp')  # 调用pygame.image.load()方法来返回一个surface
        self.rect = self.image.get_rect()  # 用get_rect()来获取相应surface的属性rect

        # 将每个外星人飞船最开始都设置在屏幕左上角附近
        self.rect.x = 0
        self.rect.y = 0

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人飞船"""  # 根据self.rect指定的位置将图像绘制到屏幕上
        self.screen.blit(self.image, self.rect)

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor)*(self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人碰到屏幕边缘，返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= (screen_rect.right-130):
            return True
        elif self.rect.left <= 0:
            return True
