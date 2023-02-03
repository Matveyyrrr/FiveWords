import os
import random
import pygame
import sys

pygame.init()

SIZE = (650, 500)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("5 букв")
WIDTH = 40
HEIGHT = 40
cell_color = "#FFFF00"
MARGIN = 10
FPS = 50
GRAVITY = 0.05
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
STAGES_1 = {0: 'stage_0.png',
              1: 'stage_1.png', 2: 'stage_3.png',
              3: 'stage_5.png', 4: 'stage_6.png',
              5: 'stage_8.png', 6: 'stage_10.png'}
STAGES_2 = {0: 'heart0.png',
            1: 'heart1.png', 2: 'heart2.png',
            3: 'heart3.png', 4: 'heart4.png',
            5: 'heart5.png', 6: 'heart6.png'}

def load_from_file(file_name):
    fname = os.path.join("text", file_name)
    if not os.path.isfile(fname):
        print(f"файл '{fname}' отсутствует, либо был удален")
        sys.exit()
    f = open(fname, "rt", encoding="utf-8")
    return [word.upper().strip() for word in f.readlines()]


def load_image(name, colorkey=None):
    fname = os.path.join("data", name)
    if not os.path.isfile(fname):
        print(f"файл '{fname}' отсутствует, либо был удален")
        sys.exit()
    img = pygame.image.load(fname)
    if colorkey is not None:
        img = img.convert()
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey)
        else:
            img = img.convert_alpha()
    return img


def draw_cell(letter, letter_col, cell_col, row, col, cell_size=40, not_filled=False):
    x = row * cell_size + (row + 1) * MARGIN
    y = col * cell_size + (col + 1) * MARGIN
    if not_filled:
        pygame.draw.rect(screen, cell_col, (y, x, WIDTH, HEIGHT), 3, 7)
    else:
        pygame.draw.rect(screen, cell_col, (y, x, WIDTH, HEIGHT), border_radius=7)
    font = pygame.font.Font(None, 40)
    text = font.render(f'{letter}', True, letter_col)
    screen.blit(text, (8 + (col + 1) * MARGIN + col * cell_size, 10 + (row + 1) * MARGIN + row * cell_size))


class Keyboard:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=40):
        alpha = "ёйцукенгшщзхъфывапролджэячсмитьбю".upper()
        self.alpha = {-1: [], 0: [], 1: [], 2: []}   # цвета клавиш
        for a in alpha:
            self.alpha[-1].append(a)
        self.width = width
        self.height = height
        self.board = [list(alpha[:11]), list(alpha[11:22]), list(alpha[22:])]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.set_view(left, top, cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):  # отрисовка клавиатуры
        for row in range(3):
            for col in range(11):
                x = (row + 7) * self.cell_size + (row + 8) * MARGIN
                y = col * self.cell_size + (col + 1) * MARGIN
                if self.board[row][col] in self.alpha[1]:       # проверяем, каким цветом рисовать клавишу
                    cell_color = (255, 255, 0)
                    text_color = (0, 0, 0)
                elif self.board[row][col] in self.alpha[2]:
                    cell_color = (255, 255, 255)
                    text_color = (0, 0, 0)
                elif self.board[row][col] in self.alpha[0]:       # проверяем, каким цветом рисовать клавишу
                    cell_color = (100, 100, 100)
                    text_color = (255, 255, 255)
                elif self.board[row][col] in self.alpha[-1]:
                    cell_color = (0, 0, 0)
                    text_color = (255, 255, 255)
                pygame.draw.rect(screen, cell_color, (y, x, WIDTH, HEIGHT), border_radius=7)
                font = pygame.font.Font(None, 40)
                text = font.render(f'{self.board[row][col]}', True, text_color)
                screen.blit(text, (self.left + (col + 1) * MARGIN + col * self.cell_size, self.top + (row + 8) * MARGIN + (row + 7) * self.cell_size))

    def get_cell(self, mouse_pos):
        y, x = mouse_pos
        x = (x - self.cell_size - MARGIN) // (self.cell_size + MARGIN) - 6
        y = (y - 7 * self.cell_size - 8 * MARGIN) // (self.cell_size + MARGIN) + 7
        if 0 <= x < 3 and 0 <= y < 11:
            return x, y

    def get_press(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            x, y = cell
            return self.on_press(x, y)

    def on_press(self, x, y):
        return self.board[x][y]


class Board:
    # создание поля
    flag = False
    def __init__(self, width, height, answers=""):
        self.cnt = 0
        self.win_or_lose = False
        self.width = width
        self.height = height
        self.board = [[""] * 5 for _ in range(6)]
        self.left = 0
        self.top = 0
        self.cell_size = 40
        self.set_view(self.left, self.top, self.cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        # answers = list(answer)
        for row in range(6):
            answers = list(answer)
            self.cnt = 0
            for col in range(5):
                if self.board[row][col] == "":
                    draw_cell(self.board[row][col], (255, 0, 255), cell_color, row, col, not_filled=True)
                elif self.board[row][col] == answer[col]:
                    self.cnt += 1
                    draw_cell(self.board[row][col], (0, 0, 0), (255, 255, 0), row, col)
                    keyboard.alpha[1].append(self.board[row][col])
                elif self.board[row][col] in answers:
                    keyboard.alpha[2].append(self.board[row][col])
                    draw_cell(self.board[row][col], (0, 0, 0), (255, 255, 255), row, col)
                else:
                    draw_cell(self.board[row][col], (255, 255, 255), (100, 100, 100), row, col)
                    keyboard.alpha[0].append(self.board[row][col])
                if self.board[row][col] in answers:
                    answers.remove(self.board[row][col])
            if self.cnt == 5:
                self.win_or_lose = True

    def win(self):
        return self.win_or_lose


class Lifes:

    def __init__(self, tries=0):
        self.tries = tries
        self.image_1 = load_image(STAGES_1[self.tries], -1)
        self.image_2 = load_image(STAGES_2[self.tries], (255, 255, 255))

    def render(self, scr, tries=0, ):
        viselica = pygame.transform.scale(self.image_1, (300, 300))
        screen.blit(viselica, (200, 2))
        hearts = pygame.transform.scale(self.image_2, (150, 30))
        screen.blit(hearts, (480, 2))

    def next_img(self, img):
        self.image_1 = load_image(STAGES_1[(self.tries) % 7], -1)
        self.image_2 = load_image(STAGES_2[(self.tries) % 7], -1)


class Word(Board):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
        self.board = ["_"] * 5

    def render(self, scr):
        for col, letter in enumerate(self.board):
            draw_cell(letter, (200, 200, 255), (50, 50, 255), 6, col)
        draw_cell("<-", cell_color, (100, 100, 100), 6, 5)
        draw_cell("\/", cell_color, (100, 100, 100), 6, 6)

    def get_cell(self, mouse_pos):
        y, x = mouse_pos
        x = (x - self.cell_size - MARGIN) // (self.cell_size + MARGIN)
        y = (y - 7 * self.cell_size - 8 * MARGIN) // (self.cell_size + MARGIN)
        if x == 5 and y == -2 or x == 5 and y == -1:
            return x, y

    def get_press(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            x, y = cell
            if x * y == -10:
                return True
            else:
                return False


class Particle(pygame.sprite.Sprite):
    screen_rect = (0, 0, SIZE[0], SIZE[1])
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20, 30):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


class Game:
    def __init__(self, board, word, keyboard):
        self.board = board
        self.word = word
        self.keyboard = keyboard

    def render(self, screen):
        self.board.render(screen)
        self.keyboard.render(screen)
        self.word.render(screen)
        if board.win():
            win_screen()
            return


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Чтобы вызвать правила игры, ",
                  "нажмите клавишу пробел",
                  "", "", "", "", "", "", "", "",
                  "Чтобы начать игру кликните мышкой"]
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.png'), SIZE)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        if text_coord < 200:
            string_rendered = font.render(line, 1, pygame.Color('white'))
        else:
            string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                help_screen()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def help_screen():
    intro_text = ["КАК ОТГАДАТЬ СЛОВО В 5 БУКВ?",
                  "",
                  "Смысл игры — подобрать правильное слово,",
                  "состоящие из пяти букв. На это каждому пользователю",
                  "предоставляется 6 попыток.  Разумеется, как и у любой",
                  "игры подобного типа, у рассматриваемого ивента имеются",
                  "свои правила, помогающие облегчить подбор букв:",
                  "1. Вводить существительное необходимо",
                  "   в единственном числе.",
                  "2. Если буква окрашена в серый цвет,",
                  "   значит, ее нет в нужном слове.",
                  "3. Если буква окрашена в белый цвет, ",
                  "   значит, она есть в слове, но стоит в другом месте.",
                  "4. Если буква окрашена в желтый цвет, значит, ",
                  "   она есть в слове и стоит в правильном месте.", ]
    clock = pygame.time.Clock()
    # fon = pygame.transform.scale(load_image('fon.png'), SIZE)
    screen.fill((100, 100, 100))
    # screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        if text_coord == 20:
            string_rendered = font.render(line, 1, pygame.Color('yellow'))
        elif text_coord >= 210:
            string_rendered = font.render(line, 1, pygame.Color('cyan'))
        else:
            string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        # string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_screen()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def win_screen():

    def create_particles(position):
        # количество создаваемых частиц
        particle_count = 40
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))

    intro_text = ["Поздравляем!", "",
                  f"Вы выиграли, это было слово {answer.strip()}",
                  ]
    clock = pygame.time.Clock()

    create_particles((SIZE[0] // 2, SIZE[1] // 2))
    create_particles((SIZE[0] // 2 - 150, SIZE[1] // 2 - 150))
    create_particles((SIZE[0] // 2 + 150, SIZE[1] // 2 - 150))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill("blue")
        all_sprites.update()
        all_sprites.draw(screen)
        viselica = pygame.transform.scale(load_image(STAGES_1[tries - 1], -1), (SIZE[0] // 2, SIZE[1] // 2))
        screen.blit(viselica, (0, 180))
        lifes = pygame.transform.scale(load_image(STAGES_2[tries - 1], "DD0D14"), (150, 30))
        screen.blit(lifes, (350, 200))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen():
    intro_text = ["GAME OVER", "",
                  f"Вы проиграли, это было слово {answer.strip()}",
                  ]
    clock = pygame.time.Clock()
    screen.fill("red")
    viselica = pygame.transform.scale(load_image('stage_10.png'), (SIZE[0] // 2, SIZE[1] // 2))
    screen.blit(viselica, (0, 180))
    lifes = pygame.transform.scale(load_image('heart6.png'), (150, 30))
    screen.blit(lifes, (350, 200))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

running = True
WORDS = load_from_file("words.txt")
NORMAL_WORDS = load_from_file("words2.txt")
win_or_lose = False
answer = random.choice(NORMAL_WORDS)
board = Board(WIDTH, HEIGHT, answers=answer[:])
keyboard = Keyboard(WIDTH, HEIGHT)
word_input = Word()
game = Game(board, word_input, keyboard)
tries = 0
lifes = Lifes()
hod = False

print(answer)
while running and tries < 6:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            word = list(input().upper())
            while len(word) != 5:
                print("Введите существительное из 5 букв")
                word = list(input().upper())
            board.board[tries] = word
            if word == answer:
                running = False
            tries += 1
            lifes.tries += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if keyboard.get_cell(event.pos):
                last = "".join(word_input.board).strip("_")
                text = (last + keyboard.get_press(event.pos)).ljust(5, "_")
                if len(text) == 5:
                    word_input.board = list(text)
                    hod = True
            if word_input.get_press(event.pos):
                last = "".join(word_input.board).strip("_")
                if len(last) > 0:
                    last = last[:-1]
                text = last.ljust(5, "_")
                if len(text) == 5:
                    word_input.board = list(text)
                    hod = True

            if word_input.get_cell(event.pos):
                if not word_input.get_press(event.pos):
                    last = "".join(word_input.board).strip("_")
                    text = list(last)
                    if len(text) == 5:
                        board.board[tries] = list(text)
                        tries += 1
                        lifes.tries += 1
                        word_input.board = ["_"] * 5
    if board.win():
        win_or_lose = True
        running = False
        win_screen()
        break

    game.render(screen)
    if running and tries > 0:
        lifes.next_img(1)
        lifes.render(screen, tries)
    pygame.display.update()
    screen.fill("#99D9EA")

if not win_or_lose:
    game_over_screen()
