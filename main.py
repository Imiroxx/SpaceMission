import pygame
from pygame.locals import *
from sys import exit
import levle
from constant import *

pygame.init()
WIN_WIDTH = 1600
WIN_HEIGHT = 1000
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Warhammer 40000 Menu")
background = pygame.image.load('Космо/fonmain.jpeg')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 150)
LIGHT_BLUE = (100, 150, 200)
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_button(surface, rect, text, base_color, hover_color, text_color, shadow_offset=5):
    mx, my = pygame.mouse.get_pos()
    hovering = rect.collidepoint((mx, my))
    shadow_rect = rect.move(shadow_offset, shadow_offset)
    pygame.draw.rect(surface, DARK_GRAY, shadow_rect, border_radius=10)
    if hovering:
        gradient = pygame.Surface((rect.width, rect.height))
        for y in range(rect.height):
            alpha = y / rect.height
            color = tuple(int(base_color[i] + (hover_color[i] - base_color[i]) * alpha) for i in range(3))
            pygame.draw.line(gradient, color, (0, y), (rect.width, y))
        gradient.set_alpha(200)
        surface.blit(gradient, rect)
    else:
        pygame.draw.rect(surface, base_color, rect, border_radius=10)
    pygame.draw.rect(surface, LIGHT_GRAY if hovering else GRAY, rect, 2, border_radius=10)
    text_obj = small_font.render(text, 1, text_color)
    text_rect = text_obj.get_rect(center=rect.center)
    surface.blit(text_obj, text_rect)


def main_menu():
    while True:
        screen.blit(background, (0, 0))
        draw_text('SpaceMission', font, WHITE, screen, WIN_WIDTH // 2 - 150, WIN_HEIGHT // 10)
        button_width, button_height = 200, 60
        start_button = pygame.Rect(WIN_WIDTH // 2 - button_width // 2, WIN_HEIGHT // 3, button_width, button_height)
        settings_button = pygame.Rect(WIN_WIDTH // 2 - button_width // 2, WIN_HEIGHT // 3 + 100, button_width, button_height)
        exit_button = pygame.Rect(WIN_WIDTH // 2 - button_width // 2, WIN_HEIGHT // 3 + 200, button_width, button_height)
        draw_button(screen, start_button, 'Start', BLUE, LIGHT_BLUE, WHITE)
        draw_button(screen, settings_button, 'Settings', BLUE, LIGHT_BLUE, WHITE)
        draw_button(screen, exit_button, 'Exit', BLUE, LIGHT_BLUE, WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_button.collidepoint((mx, my)):
                    return 'start'
                if settings_button.collidepoint((mx, my)):
                    settings_menu()
                if exit_button.collidepoint((mx, my)):
                    pygame.quit()
                    exit()
        pygame.display.update()


def game_over_screen():
    game_over_bg = pygame.image.load('Космо/game_over.png')
    game_over_bg = pygame.transform.scale(game_over_bg, (850, 600))
    font = pygame.font.Font(None, 74)
    text = font.render("Вы проиграли! Хотите начать заново?", True, WHITE)
    text_rect = text.get_rect(center=(WIN_WIDTH // 2, 650))
    button_width, button_height = 200, 60
    retry_button = pygame.Rect(WIN_WIDTH // 2 - button_width // 2, 700, button_width, button_height)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(game_over_bg, (WIN_WIDTH // 2 - 425, 50))
        screen.blit(text, text_rect)
        draw_button(screen, retry_button, 'Начать заново', BLUE, LIGHT_BLUE, WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if retry_button.collidepoint((mx, my)):
                    return 'retry'
        pygame.display.update()


def settings_menu():
    resolutions = [(800, 600), (1024, 768), (1600, 1200)]
    current_resolution = (WIN_WIDTH, WIN_HEIGHT)
    selected_resolution = resolutions.index(current_resolution)
    dropdown_open = False
    dropdown_width, dropdown_height = 300, 50
    dropdown_rect = pygame.Rect(WIN_WIDTH // 2 - dropdown_width // 2, WIN_HEIGHT // 3, dropdown_width, dropdown_height)
    dropdown_items = [pygame.Rect(WIN_WIDTH // 2 - dropdown_width // 2, WIN_HEIGHT // 3 + (i + 1) * dropdown_height, dropdown_width, dropdown_height) for i in range(len(resolutions))]
    while True:
        screen.blit(background, (0, 0))
        draw_text('Settings', font, WHITE, screen, WIN_WIDTH // 2 - 150, WIN_HEIGHT // 10)
        mx, my = pygame.mouse.get_pos()
        draw_button(screen, dropdown_rect, f'Resolution: {resolutions[selected_resolution][0]}x{resolutions[selected_resolution][1]}', BLUE, LIGHT_BLUE, WHITE)
        if dropdown_open:
            for i, res in enumerate(resolutions):
                item_rect = dropdown_items[i]
                draw_button(screen, item_rect, f'{res[0]}x{res[1]}', BLUE, LIGHT_BLUE, WHITE)
        back_button = pygame.Rect(WIN_WIDTH // 2 - 100, WIN_HEIGHT // 3 + 300, 200, 60)
        draw_button(screen, back_button, 'Back', BLUE, LIGHT_BLUE, WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint((mx, my)):
                    dropdown_open = not dropdown_open
                elif dropdown_open:
                    for i, item_rect in enumerate(dropdown_items):
                        if item_rect.collidepoint((mx, my)):
                            selected_resolution = i
                            change_resolution(resolutions[selected_resolution])
                            dropdown_open = False
                if back_button.collidepoint((mx, my)):
                    return
        pygame.display.update()


def change_resolution(resolution):
    global WIN_WIDTH, WIN_HEIGHT, screen
    WIN_WIDTH, WIN_HEIGHT = resolution
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


def game_loop():
    from constant import WIN_WIDTH as CONST_WIN_WIDTH, WIN_HEIGHT as CONST_WIN_HEIGHT, DISPLAY, BACKGROUND_COLOR, PLATFORM_WIDTH, PLATFORM_HEIGHT, MOVE_SPEED, WIDTH, HEIGHT, JUMP_POWER, GRAVITY
    from levle import home_
    from game import Platform, bg, Player, draw_map, camera_configure, Camera
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Game")
    entities = pygame.sprite.Group()
    platforms = []
    players = []
    draw_map(home_)
    total_level_width = len(home_[0]) * PLATFORM_WIDTH
    total_level_height = len(home_) * PLATFORM_HEIGHT
    camera = Camera(camera_configure, total_level_width, total_level_height)
    run = True
    right = left = up = bot = False
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                right = True
            if e.type == pygame.KEYUP and e.key == pygame.K_d:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_a:
                left = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_w:
                up = True
            if e.type == pygame.KEYUP and e.key == pygame.K_w:
                up = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                bot = True
            if e.type == pygame.KEYUP and e.key == pygame.K_s:
                bot = False
        screen.fill((0, 0, 0))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if players:
            players[0].update(left, right, up, platforms, bot)
            players[0].draw_hp(screen, camera)
            if players[0].hp <= 0:
                result = game_over_screen()
                if result == 'retry':
                    players[0].hp = 100
                    players[0].rect.x = 100
                    players[0].rect.y = 100
            camera.update(players[0])
        else:
            print("Игрок не найден! Убедитесь, что уровень содержит символ '!' для создания игрока.")
            run = False
        pygame.display.update()


def main():
    while True:
        action = main_menu()
        if action == 'start':
            game_loop()


if __name__ == "__main__":
    main()


# SpaceMission
