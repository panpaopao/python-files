import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""                                     # screen参数指定飞船要绘制在什么地方
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')                 # 调用pygame.image.load()方法来返回一个surface
        self.rect = self.image.get_rect()                                 # 用get_rect()来获取相应surface的属性rect
        self.screen_rect = screen.get_rect()                                # 将表示屏幕的矩形存储在self.screen_tect中

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx                      # 将每艘飞船的中心x坐标和屏幕的x坐标设置为相同，使飞船水平居中
        self.rect.bottom = self.screen_rect.bottom                        # 将飞船与屏幕下边缘对齐

        # 在飞船的属性center中储存小数值
        self.center = float(self.rect.centerx)
        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """在指定位置绘制飞船"""                                            # 根据self.rect指定的位置将图像绘制到屏幕上
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据移动表示来调整飞船的位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.centerx < 932:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.centerx > 18:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center来更新rect对象
        self.rect.centerx = self.center

    def center_ship(self):
        """将飞船设置在屏幕底部居中"""
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        