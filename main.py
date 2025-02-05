import random
import pygame

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Тир")

# Загрузка изображений
background = pygame.image.load('img/shooting_range_background.png')
target_img = pygame.image.load('img/target.png')
game_icon = pygame.image.load('img/shooting-range.png')
gun_cursor = pygame.image.load('img/gun.png')  # Картинка пистолета (курсор)
gun_cursor = pygame.transform.scale(gun_cursor, (90, 90))


# Отключаем стандартный курсор
pygame.mouse.set_visible(False)

# Масштабируем фон, если его размер не совпадает с экраном
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Устанавливаем иконку игры
pygame.display.set_icon(game_icon)

# Координаты правых зон для мишеней
right_zone_positions = [
    (205, 215),
    (285, 215),
    (365, 215),
    (445, 215),
    (525, 215)
]

# Ограничение максимального размера мишени
MAX_TARGET_SIZE = 100  # Максимальный размер мишени по ширине/высоте

# Масштабируем мишень, если она слишком большая
target_width, target_height = target_img.get_width(), target_img.get_height()
if target_width > MAX_TARGET_SIZE or target_height > MAX_TARGET_SIZE:
    scale_factor = min(MAX_TARGET_SIZE / target_width, MAX_TARGET_SIZE / target_height)
    target_img = pygame.transform.scale(target_img, (int(target_width * scale_factor), int(target_height * scale_factor)))

    # Случайно выбираем одну из правых зон для мишени
    target_x, target_y = random.choice(right_zone_positions)

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Проверка, попадает ли клик в область мишени
                if target_x <= mouse_x <= target_x + target_img.get_width() and target_y <= mouse_y <= target_y + target_img.get_height():
                    # Перемещаем мишень в новые случайные координаты
                    target_x, target_y = random.choice(right_zone_positions)


    # Отрисовка фона
    screen.blit(background, (0, 0))


    # Отрисовка мишени
    screen.blit(target_img, (target_x, target_y))

    # Получаем координаты мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Отображаем кастомный курсор (центрируем его, если нужно)
    cursor_offset_x, cursor_offset_y = 30, 30  # Смещение, чтобы курсор выглядел естественно
    screen.blit(gun_cursor, (mouse_x - cursor_offset_x, mouse_y - cursor_offset_y))

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
