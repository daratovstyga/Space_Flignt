import os
import random
import sys
import time
import pygame

pygame.init()
pygame.display.set_caption('Space Flight')
size = width, height = 1024, 1024
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
all_sprites = pygame.sprite.Group()
cosmic_sprites = pygame.sprite.Group()
planet_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
check_animation = 0
way = str(random.randint(1, 5))
score = 0

ways = {'1': ['4', '5'], '2': ['4', '5'], '3': ['1', '5'], '4': ['1', '2'], '5': ['1', '2']}
coord = {'1': 10, '2': 180, '3': 350, '4': 520, '5': 690}


def terminate():
    pygame.quit()
    sys.exit()


def end_screen(score):
    with open('results.txt', 'r') as file:
        data = file.read()
    if int(data) < score:
        with open('results.txt', 'w') as f:
            f.write(str(score))
            data = score

    intro_text = [f"Счет {score}", f'Лучший результат {data}']

    fon = pygame.transform.scale(load_image('data/Back.png'), (width, height))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 70)
    text_blit(screen, intro_text[0], font, pygame.Color('white'), (90, 180))
    text_blit(screen, intro_text[1], font, pygame.Color('white'), (290, 240))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def text_blit(screen, text, font, color, center_coords):
    string_rendered = font.render(text, True, color)
    intro_rect = string_rendered.get_rect()
    intro_rect.top = center_coords[1] - intro_rect.height // 2
    intro_rect.x = center_coords[0] - intro_rect.width // 2
    screen.blit(string_rendered, intro_rect)


def start_screen():
    intro_text = ["*что бы начать игру, нажмите на экран*",
                  "Уклоняйтесь от планет и астероидов в Space Flight"]

    fon = pygame.transform.scale(load_image('data/Back.png'), (width, height))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 27)
    text_blit(screen, intro_text[0], font, pygame.Color('white'), (800, 800))
    text_blit(screen, intro_text[1], font, pygame.Color('white'), (260, 180))

    font = pygame.font.SysFont('arial', 150)
    text_blit(screen, 'Space Flight', font, (240, 255, 255), (512, 512))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def gameover_screen():
    font = pygame.font.SysFont('arial', 200)
    text_blit(screen, 'Game over', font, (240, 255, 255), (512, 512))


def rand_coord(a):
    current_way = random.choice(ways[a])
    current_x = coord[current_way]
    return current_way, current_x


def load_image(name, colorkey=None):
    fullname = os.path.abspath(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Planet(pygame.sprite.Sprite):
    planets_img = ["data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Ice",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Desert",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Cracked",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Alpine - Clouds",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Alpine",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Moons",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Ocean",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Ocean - Clouds",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Poison",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Radiated",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Red Planet",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Rocky",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Tropical",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Tropical - Clouds",
                   "data/SBS - 2D Planet Pack - Small 256x256/Small 256x256/Volcanic"]

    def __init__(self, pos, way):
        super().__init__(all_sprites)
        self.add(cosmic_sprites)
        self.add(planet_sprites)
        self.ind = 0
        self.animation = []
        directory = Planet.planets_img[random.randint(0, 14)]
        for i in os.listdir(directory):
            self.animation.append(load_image(os.path.join(directory, i), -1))
        self.image = self.animation[self.ind]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos
        self.rect.y = -self.rect[3] + 100
        self.check_animation = 0
        self.radius = 128
        self.way = way
        self.init_new = True
        self.is_in_score = True

    def update(self):
        global score, speed
        if self.rect.y >= 128 and self.init_new:
            self.init_new = False
            way = new_planet(self.way)
        elif self.rect.y >= 512 and self.is_in_score:
            self.is_in_score = False
            score += 1
        self.check_animation += 1
        x, y = self.rect.x, self.rect.y
        if self.check_animation % 10 == 0:
            self.ind = (self.ind + 1) % len(self.animation)
            self.image = self.animation[self.ind]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(0, speed)


class Asteroid(pygame.sprite.Sprite):
    astr_image = ["data/small/a1", "data/small/a2", "data/small/a3",
                  "data/small/b1", "data/small/b2", "data/small/b3",
                  "data/medium/a1", "data/medium/a2", "data/medium/a3",
                  "data/medium/b1", "data/medium/b2", "data/medium/b3",
                  "data/medium/c1", "data/medium/c2", "data/medium/d1",
                  "data/medium/d2"]

    def __init__(self):
        super().__init__(all_sprites)
        self.add(cosmic_sprites)
        self.animation = []
        self.ind = 0
        directory = Asteroid.astr_image[random.randint(0, 15)]
        for i in os.listdir(directory):
            self.animation.append(load_image(os.path.join(directory, i), -1))
        self.astr = random.randint(0, 1)
        self.image = self.animation[self.ind]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 6
        self.mask = pygame.mask.from_surface(self.image)
        if self.astr == 0:
            self.rect.x = width - random.randint(0, 400)
            if self.rect.x == width:
                self.rect.y = random.randint(0, 200)
            else:
                self.rect.y = 0
        else:
            self.rect.x = 0 + random.randint(0, 400)
            if self.rect.x == 0:
                self.rect.y = random.randint(0, 200)
            else:
                self.rect.y = 0

    def update(self):
        x, y = self.rect.x, self.rect.y
        self.ind = (self.ind + 1) % len(self.animation)
        self.image = self.animation[self.ind]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)
        if self.astr == 0:
            self.rect = self.rect.move(-4, 4)
        else:
            self.rect = self.rect.move(4, 4)


class Spaceship(pygame.sprite.Sprite):
    animation = load_image("data/AngelWing_H_150x100.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Spaceship.animation
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 450
        self.rect.y = 500
        self.radius = 36

    def crash(self):
        hits = pygame.sprite.spritecollide(spaceship, cosmic_sprites, False, pygame.sprite.collide_circle)
        if hits:
            return True
        return False


def new_planet(way):
    way, x = rand_coord(way)
    Planet(x, way)
    return way


start_screen()
Planet(coord[way], way)
spaceship = Spaceship()

explosion_animation = []
directory = "data/Flame3[64x64]"
for i in os.listdir(directory):
    explosion_animation.append(load_image(os.path.join(directory, i), -1))

background_img = [load_image(
    "data/SBS - Seamless Space Backgrounds - Large 1024x1024/Large 1024x1024/Starfields/1024x1024 Starfield 1.png"),
    load_image(
        "data/SBS - Seamless Space Backgrounds - Large 1024x1024/Large 1024x1024/Starfields/1024x1024 Starfield 2.png")]

NEW_ASTEROID = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_ASTEROID, 1800)

pygame.mixer.music.load("data/02 Space Riddle.mp3")
pygame.mixer.music.play(10)

speed = 1
ind = 0
true_new_score = -1
img = len(explosion_animation)

running = True
game_continue = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == NEW_ASTEROID and game_continue:
            if random.choice((True, True, False)):
                Asteroid()
    if game_continue:
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            if 0 <= pos[0] <= 1024 - 80:
                spaceship.rect.x = pos[0]
            pygame.mouse.set_visible(False)
        if score % 3 == 1 and true_new_score:
            true_new_score = score
            speed += 0.01
        screen.fill((0, 0, 0))
        screen.blit(background_img[ind], (0, 0))
        ind = (ind + 1) % len(background_img)
        all_sprites.draw(screen)
        cosmic_sprites.update()
        if spaceship.crash():
            game_continue = False
            img = 0
    elif img < len(explosion_animation):
        screen.blit(explosion_animation[img], (spaceship.rect.x, spaceship.rect.y))
        img += 1
    elif img == len(explosion_animation):
        gameover_screen()
        img += 1
    else:
        time.sleep(2)
        pygame.mixer.music.stop()
        end_screen(score)
        running = False
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
