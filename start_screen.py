import pygame
import sys

SIZE = 24
HEIGHT = SIZE * 16
WIDTH = SIZE * 16

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((HEIGHT, WIDTH))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    with open('records.txt', 'r') as file:
        temp = file.read().split()

    text = ["LODERUNNER JUMPER", "Управление:", "стрелка влево, стрелка вправа и пробел", "",
            "Правила простые:", "", "беги, прыгай, забирай золото.", "Лучший результат:",
            str(max([int(i) for i in temp]) if temp else 0), "",
            "Нажмите любую клавишу чтобы начать"]

    fon = pygame.transform.scale(pygame.image.load(f'sprites/splash_screen.png'), (HEIGHT, WIDTH))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, SIZE)
    text_coord = SIZE * 2
    for line in text:
        string_rendered = font.render(line, 1, (255, 255, 255))
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
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()
        clock.tick(30)
