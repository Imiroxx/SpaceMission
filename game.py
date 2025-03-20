import pygame
from pygame import *
from constant import *
from main import *
import levle
import random

pygame.init()
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
width = 1600
height = 1000
screen = pygame.display.set_mode((width, height))
screen.fill((180, 255, 255))
run = True
entities = pygame.sprite.Group()
platforms = []
enemies = pygame.sprite.Group()
WIN_WIDTH = 1600
WIN_HEIGHT = 1000
MOVE_SPEED = 2
players = []
enemy = []
faerbolls = []
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 150)
LIGHT_BLUE = (100, 150, 200)
pulyas = []
GRAVNTI = 5
GRAVITY = 0.5
left = right = up = False
bos = 0


def Perevertsh(fil, t, x=True):
    if x:
        imege = pygame.image.load(fil)
        if t:
            return pygame.transform.flip(imege, False, True)
        else:
            return pygame.transform.flip(imege, True, False)
    else:
        imege = fil
        if t:
            return pygame.transform.flip(imege, False, True)
        else:
            return [imege, pygame.transform.flip(imege, True, False)]


def reload_level():
    global entities, platforms, enemies, enemy, faerbolls, pulyas, players
    entities.empty()
    platforms.clear()
    enemies.empty()
    enemy.clear()
    faerbolls.clear()
    pulyas.clear()
    players.clear()
    draw_map(levle.home_)
    if players:
        entities.add(players[0])


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2
    l = min(0, l)
    l = max(-(camera.width - WIN_WIDTH), l)
    t = max(-(camera.height - WIN_HEIGHT), t)
    t = min(0, t)
    return Rect(l, t, w, h)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, a):
        pygame.sprite.Sprite.__init__(self)
        self.a = a
        self.image = pygame.image.load('Космо/пол.png')
        self.rect = pygame.rect.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Faerboll(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Космо/fb.png')
        self.rect = pygame.rect.Rect(x, y, 30, 30)
        self.speed = 4
        self.xvel = 0
        self.yvel = 0
        self.a = a
        self.b = b

    def update(self):
        if self.b:
            if self.a == 0:
                self.rect.x -= self.speed
            if self.a == 1:
                self.rect.x += self.speed
        else:
            self.rect.y += self.speed
        if pygame.Rect.colliderect(self.rect, players[0].rect):
            players[0].take_damage(10)
            self.kill()
            if self in faerbolls:
                faerbolls.remove(self)
        for i in platforms:
            if pygame.Rect.colliderect(self.rect, i.rect):
                self.kill()
                if self in faerbolls:
                    faerbolls.remove(self)


class Pulya(pygame.sprite.Sprite):
    def __init__(self, x, y, a):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Космо/faer.png')
        self.rect = pygame.rect.Rect(x, y, 38, 12)
        self.speed = 4
        self.xvel = 0
        self.yvel = 0
        self.a = a

    def update(self):
        if self.a == 0:
            self.rect.x -= self.speed
        if self.a == 1:
            self.rect.x += self.speed
        if pygame.Rect.colliderect(self.rect, bos.rect):
            bos.hp -= 20
            self.kill()
        for i in enemy:
            if pygame.Rect.colliderect(self.rect, i.rect):
                i.hp -= 20
                self.kill()
                if self in pulyas:
                    pulyas.remove(self)
        for j in platforms:
            if pygame.Rect.colliderect(self.rect, j.rect):
                self.kill()
                if self in pulyas:
                    pulyas.remove(self)


class bg(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Космо/9981.png')
        self.rect = pygame.rect.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        super().__init__()
        self.image = pygame.image.load('Космо/boss.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rectr = pygame.Rect(1024, 1664, 2112, 1024)
        self.hp = hp
        self.max_hp = hp
        self.speed = 1
        self.health = 100
        self.agr = False
        self.fece_direcshon = LEFT
        self.last_attack_time = 0
        self.attack_cooldown = 300
        self.last_earthquake_time = 0
        self.earthquake_cooldown = 5000
        self.last_summon_time = 0
        self.summon_cooldown = 10000
        self.phase = 1
        self.shield_active = False
        self.last_shield_time = 0
        self.shield_cooldown = 10000

    def draw_hp(self, screen, camera):
        hp_bar_width = 200
        hp_bar_height = 20
        hp_ratio = self.hp / self.max_hp
        bar_x = self.rect.x + (self.rect.width - hp_bar_width) // 2
        bar_y = self.rect.y - 30
        camera_offset = camera.state.topleft
        screen_x = bar_x + camera_offset[0]
        screen_y = bar_y + camera_offset[1]
        pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, hp_bar_width, hp_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y, hp_bar_width * hp_ratio, hp_bar_height))

    def shoot_fireball(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            fireball = Faerboll(random.randint(1024, 3072), 1664, self.fece_direcshon, False)
            fireball.image = pygame.image.load('Космо/fbf.png')
            entities.add(fireball)
            faerbolls.append(fireball)
            self.last_attack_time = current_time

    def earthquake(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_earthquake_time > self.earthquake_cooldown:
            if players[0].on_ground:
                players[0].take_damage(10)
            self.last_earthquake_time = current_time

    def summon_minions(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_summon_time > self.summon_cooldown:
            minion = Enemy(self.rect.x, self.rect.y, 50)
            entities.add(minion)
            enemies.add(minion)
            enemy.append(minion)
            self.last_summon_time = current_time

    def activate_shield(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shield_time > self.shield_cooldown:
            self.shield_active = True
            self.last_shield_time = current_time
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.shield_active = False

    def update(self):
        if self.rect.x == 2600 or self.rect.x == 1500:
            self.speed = -self.speed
        if self.agr:
            self.shoot_fireball()
        self.rect.x += self.speed
        if self.hp <= 0:
            self.kill()
            self.agr = False


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Космо/зем.png')
        self.rect = pygame.Rect(x, y, 146, 190)
        self.wolk = Perevertsh(pygame.image.load('Космо/зем.png'), False, False)
        self.wolks = True
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False
        self.hp = 100
        self.armor = 1
        self.fece_direcshon = RIGHT
        self.jump_power = 20
        self.move_speed = 3

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.armor)
        self.hp -= actual_damage

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = -self.move_speed
            self.fece_direcshon = LEFT
        if right:
            self.xvel = self.move_speed
            self.fece_direcshon = RIGHT
        if not (left or right):
            self.xvel = 0
        self.yvel += GRAVITY
        if up and self.on_ground:
            self.yvel = -self.jump_power
            self.on_ground = False
        self.rect.x += self.xvel
        self.collide_x(platforms)
        self.rect.y += self.yvel
        self.on_ground = False
        self.collide_y(platforms)
        if self.fece_direcshon == RIGHT:
            self.image = self.wolk[RIGHT]
        elif self.fece_direcshon == LEFT:
            self.image = self.wolk[LEFT]

    def collide_x(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if self.xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                elif self.xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0

    def collide_y(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if self.yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                    self.on_ground = True
                elif self.yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

    def draw_hp(self, screen, camera):
        hp_bar_width = 200
        hp_bar_height = 20
        hp_ratio = self.hp / 100
        pygame.draw.rect(screen, (255, 0, 0), (10, WIN_HEIGHT - 30, hp_bar_width, hp_bar_height))  # Фон
        pygame.draw.rect(screen, (0, 255, 0), (10, WIN_HEIGHT - 30, hp_bar_width * hp_ratio, hp_bar_height))  # HP


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Космо/м.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.wolk = Perevertsh(pygame.image.load('Космо/м.png'), False, False)
        self.rect.y = y
        self.hp = hp
        self.max_hp = hp
        self.speed = 1
        self.health = 100
        self.rectr = self.image.get_rect()
        self.rectr.width = 1200
        self.agr = False
        self.fece_direcshon = LEFT
        self.last_attack_time = 0
        self.attack_cooldown = 750

    def draw_hp(self, screen, camera):
        hp_bar_width = 40
        hp_bar_height = 5
        hp_ratio = self.hp / self.max_hp
        bar_x = self.rect.x + (PLATFORM_WIDTH - hp_bar_width) // 2
        bar_y = self.rect.y + PLATFORM_HEIGHT + 5
        camera_offset = camera.state.topleft
        screen_x = bar_x + camera_offset[0]
        screen_y = bar_y + camera_offset[1]
        pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y, hp_bar_width, hp_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y, hp_bar_width * hp_ratio, hp_bar_height))

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.agr:
            if self.fece_direcshon == LEFT:
                self.rect.x -= self.speed
            elif self.fece_direcshon == RIGHT:
                self.rect.x += self.speed
            self.rectr.x = self.rect.x - 600
            self.rectr.y = self.rect.y
            if self.rect.right < 3290 or self.rect.left > 3600:
                if self.fece_direcshon == LEFT:
                    self.fece_direcshon = RIGHT
                else:
                    self.fece_direcshon = LEFT
        else:
            if players[0].rect.x > self.rect.x:
                self.fece_direcshon = RIGHT
                if not bool(faerbolls) and current_time - self.last_attack_time > self.attack_cooldown:
                    d = Faerboll(self.rect.x + 150, self.rect.y + 50, self.fece_direcshon)
                    d.image = Perevertsh('Космо/fb.png', False)
                    entities.add(d)
                    faerbolls.append(d)
                    self.last_attack_time = current_time
            elif players[0].rect.x < self.rect.x:
                self.fece_direcshon = LEFT
                if not bool(faerbolls) and current_time - self.last_attack_time > self.attack_cooldown:
                    d = Faerboll(self.rect.x - 25, self.rect.y + 50, self.fece_direcshon)
                    d.image = pygame.image.load('Космо/fb.png')
                    entities.add(d)
                    faerbolls.append(d)
                    self.last_attack_time = current_time
        if self.fece_direcshon == RIGHT:
            self.image = self.wolk[RIGHT]
        elif self.fece_direcshon == LEFT:
            self.image = self.wolk[LEFT]
        if self.hp <= 0:
            self.kill()
            enemy.remove(self)


def draw_map(map):
    global bos
    x = 0
    y = 0
    hero = None
    for row in map:
        for col in row:
            if col == "!":
                hero = Player(x, y)
                players.append(hero)
            elif col == "t":
                pf = bg(x, y)
                entities.add(pf)
            elif col == "к":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/к.png')
                entities.add(pf)
            elif col == "r":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/k+.png')
                entities.add(pf)
            elif col == "w":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/k++.png')
                entities.add(pf)
            elif col == "q":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/k-.png')
                entities.add(pf)
            elif col == "s":  # Босс
                boss = Boss(x, y, 300000)
                bos = boss
                entities.add(boss)
            elif col == "@":  # Мини-враг
                enemyl = Enemy(x, y, 150)
                entities.add(enemyl)
                enemies.add(enemyl)
                enemy.append(enemyl)
            elif col == "d":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/d.jpg')
                entities.add(pf)
            elif col == "e":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/boss.jpg')
                entities.add(pf)
            elif col == "o":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/k--.png')
                entities.add(pf)
            elif col == "a":
                pf = bg(x, y)
                pf.image = pygame.image.load('Космо/r.jpg')
                entities.add(pf)
            elif col == "-":
                pf = Platform(x, y, '-')
                entities.add(pf)
                platforms.append(pf)
            elif col == "_":
                pf = Platform(x, y, '_')
                pf.image = Perevertsh('Космо/пол.png', True)
                entities.add(pf)
                platforms.append(pf)
            elif col == "*":
                pf = Platform(x, y, '*')
                pf.image = pygame.image.load('Космо/ctena.png')
                entities.add(pf)
                platforms.append(pf)
            elif col == "+":
                pf = Platform(x, y, '+')
                pf.image = Perevertsh('Космо/ctena.png', False)
                entities.add(pf)
                platforms.append(pf)
            elif col == "/":
                pf = Platform(x, y, '/')
                pf.image = pygame.image.load('Космо/cr.jpg')
                entities.add(pf)
                platforms.append(pf)
            elif col == "l":
                pf = Platform(x, y, 'l')
                pf.image = Perevertsh('Космо/cr.jpg', True)
                entities.add(pf)
                platforms.append(pf)
            elif col == "1":
                pf = Platform(x, y, '1')
                pf.image = pygame.image.load('Космо/def.jpg')
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    if hero:
        entities.add(hero)
    elif enemy:
        entities.add(enemy)


def show_start_screen():
    intro_image = pygame.image.load('Космо/yved.jpg')
    intro_image = pygame.transform.scale(intro_image, (850, 500))
    font = pygame.font.Font(None, 36)
    mission_text = font.render("Удачи в выполнении мисси!", True, (255, 255, 255))
    button_text = font.render("Принял", True, (255, 255, 255))
    button_rect = pygame.Rect(WIN_WIDTH // 2 - 100, WIN_HEIGHT - 200, 200, 50)
    button_color = (0, 128, 0)
    button_hover_color = (0, 200, 0)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    intro = False
        screen.fill((0, 0, 0))
        screen.blit(intro_image, (WIN_WIDTH // 2 - 400, 50))
        screen.blit(mission_text, (WIN_WIDTH // 2 - mission_text.get_width() // 2, WIN_HEIGHT - 300))
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, (button_rect.x + (200 - button_text.get_width()) // 2,
                                  button_rect.y + (50 - button_text.get_height()) // 2))
        pygame.display.update()


pygame.init()
show_start_screen()
right = left = up = bot = False
draw_map(levle.home_)
total_level_width = len(levle.home_[0]) * PLATFORM_WIDTH
total_level_height = len(levle.home_) * PLATFORM_HEIGHT
camera = Camera(camera_configure, total_level_width, total_level_height)


def game_over_screen():
    game_over_bg = pygame.image.load('Космо/game_over.png')
    game_over_bg = pygame.transform.scale(game_over_bg, (850, 400))
    font = pygame.font.Font(None, 74)
    text = font.render("Вы проиграли! Хотите начать заново?", True, WHITE)
    text_rect = text.get_rect(center=(WIN_WIDTH // 2, 650))
    button_width, button_height = 300, 60
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


def victory_screen():
    victory_bg = pygame.image.load('Космо/victory.png')
    victory_bg = pygame.transform.scale(victory_bg, (850, 400))
    font = pygame.font.Font(None, 74)
    text = font.render("Поздравляем! Вы выполнили миссию!", True, WHITE)
    text2 = font.render("Вы прошли игру!", True, WHITE)
    text_rect = text.get_rect(center=(WIN_WIDTH // 2, 600))
    text_rect2 = text2.get_rect(center=(WIN_WIDTH // 2, 650))
    button_width, button_height = 300, 60
    exit_button = pygame.Rect(WIN_WIDTH // 2 - button_width // 2, 700, button_width, button_height)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(victory_bg, (WIN_WIDTH // 2 - 425, 50))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        draw_button(screen, exit_button, 'Выйти', BLUE, LIGHT_BLUE, WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if exit_button.collidepoint((mx, my)):
                    pygame.quit()
                    exit()
        pygame.display.update()


while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.USEREVENT + 1:
            for boss in entities:
                if isinstance(boss, Boss):
                    boss.handle_event(e)
        if e.type == pygame.MOUSEBUTTONDOWN:
            if players[0].fece_direcshon == 1:
                d = Pulya(players[0].rect.x + 150, players[0].rect.y + 73, players[0].fece_direcshon)
                entities.add(d)
                pulyas.append(d)
            if players[0].fece_direcshon == 0:
                d = Pulya(players[0].rect.x - 20, players[0].rect.y + 73, players[0].fece_direcshon)
                entities.add(d)
                pulyas.append(d)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                left = True
            if e.key == pygame.K_d:
                right = True
            if e.key == pygame.K_SPACE:
                up = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                left = False
            if e.key == pygame.K_d:
                right = False
            if e.key == pygame.K_SPACE:
                up = False
    players[0].update(left, right, up, platforms)
    for i in enemy:
        if pygame.Rect.colliderect(players[0].rect, i.rectr):
            i.agr = True
        else:
            i.agr = False
    if pygame.Rect.colliderect(players[0].rect, bos.rectr):
        bos.agr = True
        print(0)
    else:
        bos.agr = False
    bos.update()
    screen.fill((0, 0, 0))
    for e in entities:
        screen.blit(e.image, camera.apply(e))
    for i in faerbolls:
        i.update()
    for j in pulyas:
        j.update()
    players[0].draw_hp(screen, camera)
    bos.draw_hp(screen, camera)
    if bos.hp <= 0:
        victory_screen()
        run = False
    if players[0].hp <= 0:
        result = game_over_screen()
        if result == 'retry':
            reload_level()
            players[0].hp = 100
            players[0].rect.x = 576
            players[0].rect.y = 836
        elif result == 'menu':
            run = False
    for enemyl in enemies:
        enemyl.update()
        enemyl.draw_hp(screen, camera)
    camera.update(players[0])
    pygame.display.update()


# SpaceMission
