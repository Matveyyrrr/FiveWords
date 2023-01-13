import os
import random

import pygame
import sys

pygame.init()

SIZE = (700, 450)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("5 букв")
WIDTH = 40
HEIGHT = 40
cell_color = "#FFFF00"
MARGIN = 10
FPS = 50
LETTER_COLORS = {
    1: (255, 255, 255),
    2: (255, 180, 0),
    3: ()
}

#NORMAL_WORDS = None


def load_from_file(file_name):
    f = open(file_name, "r", encoding="utf-8")
    return f.readlines()


STAGES = {0: 'stage_0.png', 1: 'stage_1.png',
          2: 'stage_2.png', 3: 'stage_3.png',
          4: 'stage_4.png', 5: 'stage_5.png',
          6: 'stage_6.png', 7: 'stage_7.png',
          8: 'stage_8.png', 9: 'stage_9.png',
          10: 'stage_10.png', }

help(pygame.draw.rect)
def load_image(name, colorkey=None):
    fname = os.path.join("data", name)
    if not os.path.isfile(fname):
        print("Такого файла нет")
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
    screen.blit(text, (10 + (col + 1) * MARGIN + col * cell_size, 10 + (row + 1) * MARGIN + row * cell_size))



class Board:
    # создание поля
    def __init__(self, width, height, left=10, top=10, cell_size=40):
        self.width = width
        self.height = height
        self.board = [[""] * 5 for _ in range(6)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.set_view(left, top, cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        for row in range(6):
            for col in range(5):
                if self.board[row][col] == "":
                    draw_cell(self.board[row][col], (255, 0, 255), cell_color, row, col, not_filled=True)
                elif self.board[row][col] in answer[col]:
                    draw_cell(self.board[row][col], (0, 0, 0), (255, 255, 0), row, col)
                elif self.board[row][col] in answer:
                    draw_cell(self.board[row][col], (0, 0, 0), (255, 255, 255), row, col)
                else:
                    draw_cell(self.board[row][col], (255, 255, 255), (100, 100, 100), row, col)


    def get_cell(self, mouse_pos):
        y, x = mouse_pos
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if 0 <= y < self.width and 0 <= x < self.height:
            return x, y

    def get_press(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_press(cell)

    def on_press(self, cell_coords):
        print(cell_coords)

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Чтобы вводить новое слово, ",
                  "нажмите клавишу пробел",
                  "",
                  "Чтобы начать игру кликните мышкой"]
    # pygame.init()
    clock = pygame.time.Clock()
    #fon = pygame.transform.scale(load_image('fon.jpg'), SIZE)
    #screen.blit(fon, (0, 0))
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
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def end_screen():
    intro_text = ["GAME OVER", "",
                  "Вы проиграли",
                  "Чтобы начать новую игру, ",
                  "нажмите клавишу пробел",
                  ]
    # pygame.init()
    clock = pygame.time.Clock()
    #fon = pygame.transform.scale(load_image('fon.jpg'), SIZE)
    #screen.blit(fon, (0, 0))
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
                start_screen()
                return
        pygame.display.flip()
        clock.tick(FPS)

start_screen()
NOUNS = load_from_file("Text/words.txt")

running = True
board = Board(WIDTH, HEIGHT)
tries = 0
answer = random.choice(NOUNS)
while running and tries < 6:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or tries == 6:
            running = False
            end_screen()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            word = list(input().upper())
            while len(word) != 5:
                print("Введите существительное из 5 букв")
                word = list(input().upper())
            board.board[tries] = word
            tries += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_press(event.pos)

    board.render(screen)
    pygame.display.update()
    screen.fill((0, 0, 0))