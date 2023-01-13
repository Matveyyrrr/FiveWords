import pygame
import sys


def text(self):
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode
        if active:
            color = self.color_active
        else:
            color = self.color_passive

        pygame.draw.rect(self.display_screen, color, self.input_rect)
        text_surface = self.base_font.render(user_text, True, (255, 255, 255))
        self.display_screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)


pygame.init()

FPS = 60
clock = pygame.time.Clock()

size = (290, 310)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game Five Words")
pygame.display
wight = 40
hight = 40
waiht = (0, 0, 0)
margin = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for col in range(5):
        for row in range(6):
            y = row * hight + (row + 1) * margin
            x = col * wight + (col + 1) * margin
            pygame.draw.rect(screen, waiht, (x, y, wight, hight), 3, 4)
    pygame.display.update()
    screen.fill((200, 200, 200))