import random

import pygame

# Константы

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
target_img = pygame.image.load('img/target.png')
game_icon = pygame.image.load('img/shooting_range.png')
target_x = random.randint(0, SCREEN_WIDTH - target_img.get_width())
target_y = random.randint(0, SCREEN_HEIGHT - target_img.get_height())
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка фонового изображения
background = pygame.image.load("shooting_range_background.png")

pygame.display.set_caption("Игра Тир")

pygame.display.set_icon(game_icon)



pygame.init()


pygame.quit()
