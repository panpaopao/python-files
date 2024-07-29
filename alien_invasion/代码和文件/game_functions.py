import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) <= ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, bullets, aliens, score_count):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(aliens, bullets, ai_settings, screen, ship, stats,
                              play_button, mouse_x, mouse_y, score_count)


def check_play_button(aliens, bullets, ai_settings, screen, ship, stats, play_button, mouse_x, mouse_y, score_count):
    """玩家点击Play按钮开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:    # 当检测到按钮按下并且游戏处于活动状态时，隐藏按钮，只有在开始时才会生效

        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        """重置游戏统计信息"""
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌和等级图像
        score_count.prep_score()
        score_count.prep_highest_score()
        score_count.prep_level()
        score_count.prep_ships()

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, score_count):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()                      # 将飞船绘制到屏幕上，保证它出现在背景前面
    aliens.draw(screen)

    # 绘制得分
    score_count.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()                       # 每次执行while循环，都会绘制一个新屏幕并且擦去旧屏幕，只有新屏幕可见，屏幕不断更新


def update_bullets(ai_settings, aliens, screen, ship, bullets, stats, score_count):
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, score_count)


def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, score_count):
    # 检查是否有子弹击中了外星人，如果有，则删除子弹以及相应的外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.scores += ai_settings.alien_points
        score_count.prep_score()
        check_highest_score(stats, score_count)
        pygame.mixer.init()
        channel = pygame.mixer.Channel(2)
        sound = pygame.mixer.Sound('boom1.wav')
        channel.play(sound)

    if len(aliens) == 0:
        """删除现有的子弹并新建另一批外星人"""
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings, screen, ship, aliens)

        # 提高等级
        stats.level += 1
        score_count.prep_level()

    if len(aliens) <= 8:
        ai_settings.change_alien_drop_speed()                  # 如果外星人的飞船数量不超过8，则下降速度加快
    else:
        ai_settings.recover_alien_drop_speed()                 # 打完飞船后更新飞船，则下降速度恢复原值


def check_highest_score(stats, score_count):
    if stats.scores >= score_count.highest_score:
        score_count.highest_score = stats.scores
        with open('highest_score.txt', 'w') as file_object:
            file_object.write(str(score_count.highest_score))
        score_count.prep_highest_score()


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, score_count):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到时一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, score_count)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变其方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= (-1)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, score_count):
    """检查是否有外星人位于屏幕边缘，并调整所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人是否与飞船发生碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, score_count)
    # 检测外星人是否到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, score_count)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, score_count):
    """响应被外星人撞到的飞船"""

    # 将ship_left减1
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        """重置游戏统计信息"""
        stats.reset_stats()
        stats.game_active = True

        # 更新记分牌
        score_count.prep_ships()
        score_count.prep_score()
        score_count.prep_highest_score()
        score_count.prep_level()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        ai_settings.initialize_dynamic_settings()  # 每次失败后速度又恢复原值

        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(1.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)                 # 当飞船全部用完后，游戏处于非活动状态，可以再次按下按钮开始下一局


def creat_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人飞船，并计算一行可以容纳多少外星人飞船
    # 外星人飞船间距等于其宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_aliens_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳多少个外星人"""
    available_space_x = ai_settings.screen_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_aliens_rows(ai_settings, ship_height, alien_height):
    """计算可以容纳多少行"""
    available_space_y = ai_settings.screen_height - 3 * alien_height-ship_height
    number_rows = int(available_space_y/(1.1 * alien_height))
    return number_rows


def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = 2 * alien_width * alien_number + 20
    alien.rect.x = alien.x
    alien.rect.y = 1.5 * alien.rect.height * row_number
    aliens.add(alien)
