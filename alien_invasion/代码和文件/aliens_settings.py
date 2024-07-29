class Settings():
    """存储《外星人入侵》的所有类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置，包括三个属性：屏幕的宽、屏幕的高（单位都是像素）、屏幕的背景色
        self.screen_width = 950
        self.screen_height = 650
        self.bg_color = (3, 34, 92)

        # 飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # 子弹的设置
        """创建宽3像素，高15像素的深灰色子弹，子弹的速度比飞船稍低"""
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        # 设置屏幕上允许出现的最大子弹数量
        self.bullets_allowed = 5

        # 外星人设置
        self.alien_speed_factor = 0.4
        self.alien_drop_speed = 2
        self.fleet_direction = 1                  # 1表示右移，-1表示左移
        self.alien_points = 50                          # 每个外星人值50点
        self.alien_points_increase = 1.5                # 外星人点数的提高速度

        # 以什么样的速度加快游戏
        self.speedup = 1.1

        self.initialize_dynamic_settings()

    def change_alien_drop_speed(self):
        self.alien_drop_speed = 10

    def recover_alien_drop_speed(self):
        self.alien_drop_speed = 2

    def initialize_dynamic_settings(self):
        """初始化随游戏变化而改变的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.4
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup
        self.bullet_speed_factor *= self.speedup
        self.alien_speed_factor *= self.speedup
        self.fleet_direction *= self.speedup
        self.alien_points = int(self.alien_points * self.alien_points_increase)
