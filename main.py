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
pygame.display.set_caption('Игра "Тир"')

# Загрузка изображений
background = pygame.image.load('img/shooting_range_background.png')
target_img = pygame.image.load('img/target.png')
game_icon = pygame.image.load('img/shooting-range.png')
gun_cursor = pygame.image.load('img/gun.png')  # Картинка пистолета (курсор)
bullet_hole_img = pygame.image.load('img/hole.png')  # Загружаем отверстие от пули
muzzle_flash_img = pygame.image.load('img/flash.png')  # Вспышка выстрела

# Масштабируем изображения
bullet_hole_img = pygame.transform.scale(bullet_hole_img, (40, 40))
muzzle_flash_img = pygame.transform.scale(muzzle_flash_img, (200, 112))  # Размер вспышки

# Загрузка звука выстрела
shot_sound = pygame.mixer.Sound('img/shoot.wav')  # Замените на путь к вашему звуковому файлу

# Загрузка и воспроизведение фоновой музыки
pygame.mixer.music.load('img/background_music.mp3')  # Замените на путь к вашему mp3-файлу
pygame.mixer.music.set_volume(0.5)  # Уровень громкости (0.0 - 1.0)
pygame.mixer.music.play(-1)  # Бесконечное повторение музыки

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

# Вспышка выстрела
flash_visible = False
flash_time = 0
flash_x, flash_y = 0, 0

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

# Шрифт для отображения счета
score_font = pygame.font.SysFont('Arial', 48, bold=True)

# Координаты дула пистолета (смещение относительно верхней середины курсора)
GUN_BARREL_OFFSET_X = 47
GUN_BARREL_OFFSET_Y = 17

# Время до следующего обновления мишени
next_target_update = pygame.time.get_ticks() + random.randint(1000, 3000)  # Следующее обновление через 1-3 секунды

# Позиция кнопки выхода
exit_button_width = 100
exit_button_height = 100
exit_button_x = 10
exit_button_y = SCREEN_HEIGHT - exit_button_height - 10

# Загрузка изображения кнопки выхода
exit_button_img = pygame.image.load('img/exit_button.png')  # Замените на путь к вашей картинке кнопки
exit_button_img = pygame.transform.scale(exit_button_img, (exit_button_width, exit_button_height))  # Масштабируем до 200x200

# Список для хранения текстов на экране

floating_texts = []

# Список для хранения отверстий от пуль

bullet_holes = []  # (x, y, время появления)

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.button == 1:  # Левая кнопка мыши
                mouse_x, mouse_y = pygame.mouse.get_pos()
                aim_x = mouse_x
                aim_y = mouse_y - GUN_BARREL_OFFSET_Y - 10

                center_x = target_x + 100 // 2
                center_y = target_y + 100 // 2

                points = calculate_score(aim_x, aim_y, center_x, center_y)

                # Вспышка выстрела
                flash_x, flash_y = aim_x-65, aim_y-130
                flash_visible = True
                flash_time = current_time + 100  # Вспышка исчезнет через 100 мс

                # Добавляем координаты попадания в список bullet_holes
                bullet_holes.append((aim_x - 10, aim_y - 10, pygame.time.get_ticks()))


                # Определяем текст сообщения
                if points == 0:
                    text = "Мимо!"
                elif points == 10:
                    text = "10 очков. В яблочко!"
                else:
                    text = f"{points} очков"

                # Добавляем сообщение (текст, координаты, время появления, прозрачность)
                floating_texts.append([text, target_x + 50, target_y + 110, pygame.time.get_ticks(), 255])

                shot_sound.play()

                if points > 0:
                    target_x, target_y = random.choice(right_zone_positions)

        # Проверка, нужно ли обновить мишень
        if pygame.time.get_ticks() > next_target_update:
            target_x, target_y = random.choice(right_zone_positions)
            next_target_update = pygame.time.get_ticks() + random.randint(1000,
                                                                          5000)  # Устанавливаем новый случайный интервал от 1 до 3 секунд

        # Проверка нажатия на кнопку выхода
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (exit_button_x <= mouse_x <= exit_button_x + exit_button_width and
                    exit_button_y <= mouse_y <= exit_button_y + exit_button_height):
                running = False

    # Отрисовка фона
    screen.blit(background, (0, 0))

    # Отрисовка мишени
    screen.blit(target_img, (target_x, target_y))

    # Отображение вспышки
    if flash_visible and current_time < flash_time:
        screen.blit(muzzle_flash_img, (flash_x, flash_y))
    else:
        flash_visible = False

    # Получаем координаты мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()


    # Отображение счета на экране
    score_text = score_font.render(f"Счет: {score}", True, (255, 0, 0))  # Белый цвет
    shadow_text = score_font.render(f"Счет: {score}", True, (0, 0, 0))  # Черная тень

    # Центрируем текст сверху
    text_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
    text_y = 20  # Отступ сверху

    # Отрисовка тени для лучшей читаемости
    screen.blit(shadow_text, (text_x + 2, text_y + 2))
    screen.blit(score_text, (text_x, text_y))

    # Проверка, если курсор находится над кнопкой выхода
    if (exit_button_x <= mouse_x <= exit_button_x + exit_button_width and
            exit_button_y <= mouse_y <= exit_button_y + exit_button_height):
        pygame.mouse.set_visible(True)  # Стандартный курсор при наведении
    else:
        pygame.mouse.set_visible(False)  # Кастомный курсор

    # Отображаем кастомный курсор, если он не скрыт
    if pygame.mouse.get_visible() == False:
        screen.blit(gun_cursor, (mouse_x - CURSOR_WIDTH // 2, mouse_y - CURSOR_HEIGHT // 2))

    # Отображаем картинку кнопки выхода
    screen.blit(exit_button_img, (exit_button_x, exit_button_y))

    # Отображаем текст на экране

    current_time = pygame.time.get_ticks()
    for text_data in floating_texts[:]:
        text, x, y, start_time, alpha = text_data
        elapsed_time = current_time - start_time

        if elapsed_time > 1000:  # Через 1.5 сек удаляем текст
            floating_texts.remove(text_data)
            continue

        alpha = max(0, 255 - (elapsed_time // 6))  # Затухание
        text_surface = score_font.render(text, True, (255, 0, 0))
        text_shadow = score_font.render(text, True, (0, 0, 0))  # Черная тень
        text_surface.set_alpha(alpha)
        text_shadow.set_alpha(alpha)

        screen.blit(text_shadow, ((SCREEN_WIDTH // 2 - text_surface.get_width() // 2) + 2, y - 180 + 2))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, y-180))

    # Отображение отверстий от пуль
    current_time = pygame.time.get_ticks()
    for hole in bullet_holes[:]:
        x, y, time = hole
        if current_time - time > 1500:  # Метка исчезает через 1.5 сек
            bullet_holes.remove(hole)
        else:
            screen.blit(bullet_hole_img, (x, y))  # Отображаем отверстие от пули
    # Обновление экрана
    pygame.display.flip()


# Завершение Pygame
pygame.quit()
