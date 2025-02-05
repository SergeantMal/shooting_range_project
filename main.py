import random
import pygame
import math  # Для вычисления расстояния

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

# Размер курсора (например, 90x90 пикселей)
CURSOR_WIDTH = 90
CURSOR_HEIGHT = 83
gun_cursor = pygame.transform.scale(gun_cursor, (CURSOR_WIDTH, CURSOR_HEIGHT))

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

# Очки игрока
score = 0
font = pygame.font.Font(None, 36)  # Шрифт для отображения счета

# Координаты дула пистолета (смещение относительно верхней середины курсора)
GUN_BARREL_OFFSET_X = 47
GUN_BARREL_OFFSET_Y = 17

# Функция расчета очков в зависимости от попадания
def calculate_score(aim_x, aim_y, center_x, center_y):
    global score
    # Рассчитываем расстояние от "дула" до центра мишени
    distance = math.sqrt((aim_x - center_x) ** 2 + (aim_y - center_y) ** 2)

    # Определяем очки (10 - за попадание в центр, 1 - по краям)
    max_radius = target_img.get_width() // 2  # Радиус мишени
    if distance <= max_radius:
        points = max(1, 10 - int(distance / (max_radius / 10)))  # Чем ближе к центру, тем больше очков
        score += points
    else:
        points = 0  # Промах

    return points

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
                # Определяем координаты дула пистолета (верхняя середина курсора)
                aim_x = mouse_x
                aim_y = mouse_y - GUN_BARREL_OFFSET_Y

                # Координаты центра мишени
                center_x = target_x + 100 // 2
                center_y = target_y + 100 // 2

                # Для отладки выводим координаты центра мишени и дула пистолета
                print(f"Центр мишени: ({center_x}, {center_y})")
                print(f"Координаты дула курсора: ({aim_x}, {aim_y})")

                points = calculate_score(aim_x, aim_y, center_x, center_y)  # Подсчет очков
                print(f"Вы набрали: {points} очков! Общий счет: {score}")

                # Если попадание засчитано (очки больше 0), обновляем позицию мишени
                if points > 0:
                    target_x, target_y = random.choice(right_zone_positions)

    # Отрисовка фона
    screen.blit(background, (0, 0))

    # Отрисовка мишени
    screen.blit(target_img, (target_x, target_y))

    # Получаем координаты мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Отображаем кастомный курсор
    screen.blit(gun_cursor, (mouse_x - CURSOR_WIDTH // 2, mouse_y - CURSOR_HEIGHT // 2))

    # Обновление экрана
    pygame.display.flip()


# Завершение Pygame
pygame.quit()
