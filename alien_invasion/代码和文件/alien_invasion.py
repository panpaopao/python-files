import pygame  # 模块pygame包含开发游戏所需要的功能（2D平面）
from ship import Ship  # 导入飞船的类
import game_functions as gf  # 导入游戏有关的类
from pygame.sprite import Group
from aliens_settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import sys


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def run_game():
    # pygame.mixer.init()
    # if pygame.mixer.music.get_busy() == False:
    #     pygame.mixer.music.load('火蓝刀锋动感背景乐-纯音乐-51568134.mp3')
    #     pygame.mixer.music.play()
    # 初始化pygame、设置和屏幕对象
    pygame.init()  # pygame.init():初始化背景设置，让Pygame能够正常工作
    ai_settings = Settings()  # 通过设置类创建外星人的实例，包含屏幕宽、高、颜色三个属性
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # 创建窗口——调用pygame.display.set_mode来创建一个名为screen的窗口,尺寸通过创建实例调用类来确定
    pygame.display.set_caption("Alien Invasion")  # 给创建的窗口命名，显示在界面上方

    # 创建一个按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个用于存储外星人的编组
    aliens = Group()

    # 创建外星人群
    gf.creat_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建记分牌
    score_count = Scoreboard(ai_settings, screen, stats)

    # 开始主游戏的循环
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, bullets, aliens, score_count)  # 监视键盘和鼠标事件
        if stats.game_active:
            ship.update()
            """更新屏幕上的图像，并切换到新屏幕"""
            gf.update_bullets(ai_settings, aliens, screen, ship, bullets, stats, score_count)  # 包括处理子弹撞到飞船的事件
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, score_count)
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, score_count)


run_game()
