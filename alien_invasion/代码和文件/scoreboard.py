import pygame
from ship import Ship
from pygame.sprite import Group
filename='highest_score.txt'


class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分面板的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.ai_settings = ai_settings

        # 设置显示得分的字体设置
        self.text_color = (255, 255, 0)
        self.font = pygame.font.SysFont(None, 25)

        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()
        # 利用文本文档存储最高分，这样即使游戏关闭后，仍然能够保存最高分的数据，同时将最高分数据保存在类的初始属性中
        # 这样每次新建实例后，都能够及时获取文件中的最高分值
        with open('highest_score.txt', 'r') as file_object:
            self.highest_score = int(file_object.readline())

    def prep_score(self):
        """将得分数字由文本渲染为图像，并使其在按钮上居中"""
        rounded_scores = int(round(self.stats.scores, -1))
        score_str_now = "{:,}".format(rounded_scores)
        score_str = "scores:" + score_str_now
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right-10
        self.score_image_rect.top = 20

    def prep_highest_score(self):
        """将最高得分数字由文本渲染为图像，并使其在按钮上居中"""
        with open('highest_score.txt', 'r') as file_object:
            self.highest_score = int(file_object.readline())
            rounded_high_scores = int(round(self.highest_score, -1))
            highest_score_str = "record:" + str(rounded_high_scores)
        # highest_score=int(round(self.stats.highest_score,-1))
        # highest_score_str_now="{:,}".format(highest_score)
        # highest_score_str="record:"+highest_score_str_now
        self.highest_score_image = self.font.render(highest_score_str, True, self.text_color, self.ai_settings.bg_color)
        self.highest_score_image_rect = self.highest_score_image.get_rect()
        self.highest_score_image_rect.right = self.screen_rect.right-10
        self.highest_score_image_rect.top = 100

    def show_score(self):
        """在屏幕上显示当前得分和最高得分以及等级"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_image_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render("level:" + str(self.stats.level),
                                            True, self.text_color, self.ai_settings.bg_color)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right-10
        self.level_rect.top = 180

    def prep_ships(self):
        """显示余下还有多少艘飞船"""
        self.ships = Group()
        for ship_number in range(int(self.stats.ship_left)):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 800+ship_number*0.8*ship.rect.width
            ship.rect.y = 260
            self.ships.add(ship)
