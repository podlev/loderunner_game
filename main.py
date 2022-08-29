import pygame
import level_generator
import start_screen
import random

SIZE = 24  # Базовый размер спрайта, не менять
HEIGHT = SIZE * 16
WIDTH = SIZE * 16

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((HEIGHT, WIDTH))

game_over_sound = pygame.mixer.Sound('sprites/game-over.mp3')


def save_records():
    with open('records.txt', 'r') as file:
        temp = file.read().split()
    with open('records.txt', 'w') as file:
        file.write('\n'.join(temp) + '\n' + str(score) + '\n')


def render_level():
    global player
    with open('level.txt') as file:
        level = file.read().split()
        level = level[::-1]
        # print(level)
        for y in range(len(level)):
            for x in range(len(level[0])):
                if level[y][x] == 'b':
                    bricks.append(Bricks(random.choice(['brick_un.png', 'brick_mut.png']), y, x))
                elif level[y][x] == 'g':
                    golds.append(Golds('gold.png', y, x))
                elif level[y][x] == 'p':
                    player = Player(y, x)


class Camera:
    """класс камеры"""

    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj, speed=1):
        obj.rect.y += speed


class Bricks(pygame.sprite.Sprite):
    def __init__(self, elem, y, x):
        super().__init__(sprites_group)
        img = pygame.image.load(f'sprites/{elem}')
        self.image = pygame.transform.scale(img, (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * SIZE
        self.rect.y = HEIGHT // 2 - y * SIZE


class Golds(pygame.sprite.Sprite):
    def __init__(self, elem, y, x):
        super().__init__(sprites_group)
        img = pygame.image.load(f'sprites/{elem}')
        self.image = pygame.transform.scale(img, (SIZE // 4, SIZE // 4))
        self.rect = self.image.get_rect()
        self.rect.x = x * SIZE
        self.rect.y = HEIGHT // 2 - y * SIZE + SIZE - self.rect.height


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x):
        super().__init__(sprites_group)
        self.anim_right = [pygame.transform.scale(pygame.image.load(f'sprites/right{i}.png'), (SIZE, SIZE)) for i in
                           range(1, 5)]
        self.anim_left = [pygame.transform.scale(pygame.image.load(f'sprites/left{i}.png'), (SIZE, SIZE)) for i in
                          range(1, 5)]
        self.anim_rightup = [pygame.transform.scale(pygame.image.load(f'sprites/rightup{i}.png'), (SIZE, SIZE)) for i in
                             range(1, 5)]
        self.anim_leftup = [pygame.transform.scale(pygame.image.load(f'sprites/leftup{i}.png'), (SIZE, SIZE)) for i in
                            range(1, 5)]
        self.anim_stop = pygame.transform.scale(pygame.image.load(f'sprites/player.png'), (SIZE, SIZE))
        self.anim_down = pygame.transform.scale(pygame.image.load(f'sprites/down.png'), (SIZE, SIZE))
        self.jump_sound = pygame.mixer.Sound('sprites/jump.mp3')
        self.gold_sound = pygame.mixer.Sound('sprites/rings.mp3')
        self.image = self.anim_stop
        self.rect = self.image.get_rect()
        self.rect.x = x * 24
        self.rect.y = HEIGHT // 2 - y * 24
        self.dx = 0
        self.dy = 0
        self.speed_x = 1
        self.speed_y = 16
        self.onGround = False
        self.index_animation = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.dx += self.speed_x
            if self.dx > SIZE // 4:
                self.dx = SIZE // 4
        elif keys[pygame.K_LEFT]:
            self.dx -= self.speed_x
            if self.dx < -SIZE // 4:
                self.dx = -SIZE // 4
        else:
            self.dx = 0

        if keys[pygame.K_SPACE] and self.can_jump():
            self.dy -= self.speed_y
            self.jump_sound.play()

        if not self.onGround:
            self.dy += 1

        self.animation(self.dx, self.dy)
        self.rect.x += self.dx
        self.collider_x()
        self.rect.y += self.dy
        self.collider_y()
        self.golds_up()

    def animation(self, dx, dy):
        if dy == 1:
            if dx > 0:
                self.image = self.anim_right[self.index_animation]
            elif dx < 0:
                self.image = self.anim_left[self.index_animation]
            else:
                self.image = self.anim_stop
                self.index_animation = 0
            self.index_animation += 1
            if self.index_animation > 3:
                self.index_animation = 0
        else:
            if dy < 1 and dx > 0:
                self.image = self.anim_rightup[self.index_animation]
            if dy < 1 and dx < 0:
                self.image = self.anim_leftup[self.index_animation]
            if dy > 1:
                self.image = self.anim_down
            self.index_animation += 1
            if self.index_animation > 3:
                self.index_animation = 0

    def can_jump(self):
        self.rect.y += 10
        for b in bricks:
            if pygame.sprite.collide_rect(player, b):
                self.rect.y -= 10
                return True
        self.rect.y -= 10
        return False

    def collider_x(self):
        for b in bricks:
            if pygame.sprite.collide_rect(player, b):
                if self.dx > 0:
                    player.rect.right = b.rect.left
                if self.dx < 0:
                    player.rect.left = b.rect.right
        if self.rect.x + self.rect.width >= WIDTH:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x <= 0:
            self.rect.x = 0

    def collider_y(self):
        for b in bricks:
            if pygame.sprite.collide_rect(player, b):
                if self.dy > 0:
                    player.rect.bottom = b.rect.top
                if self.dy < 0:
                    player.rect.top = b.rect.bottom
                self.dy = 0
                self.onGround = True
        else:
            self.onGround = False

    def golds_up(self):
        global score
        for g in range(len(golds)):
            if pygame.sprite.collide_rect(player, golds[g]):
                Golds.kill(golds[g])
                del golds[g]
                score += 50
                self.gold_sound.play()
                break

    def game(self):
        if self.rect.top >= HEIGHT:
            font = pygame.font.Font(None, SIZE)
            s = f'ВЫ ПРОИГРАЛИ. ОЧКИ: {score}'
            text = font.render(s, 1, (255, 255, 255))
            screen.blit(text, (50, HEIGHT // 2))
            pygame.draw.rect(screen, (128, 128, 128),
                             (50, HEIGHT // 2 - 10, text.get_width() + 20, text.get_height() + 20), 1)
            return False
        else:
            font = pygame.font.Font(None, SIZE)
            text = font.render(f'ОЧКИ: {score}', 1, (255, 255, 255))
            screen.blit(text, (4, 4))
        return True

    def speed(self):
        return self.rect.y


while True:
    sprites_group = pygame.sprite.Group()
    bricks = []
    golds = []
    score = 0
    player = None
    start_screen.start_screen()
    level_generator.level_generator()
    render_level()
    camera = Camera()
    run = True
    base_speed = SIZE // 24

    while run:
        game_over_sound.stop()
        screen.fill(pygame.Color(0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for sprite in sprites_group:
            camera.apply(sprite, speed=base_speed)

        if score > 2400:
            base_speed = SIZE // 6
        elif score > 1600:
            base_speed = SIZE // 8
        elif score > 800:
            base_speed = SIZE // 12

        # print(base_speed)
        sprites_group.draw(screen)
        player.update()
        player.game()
        pygame.display.flip()
        clock.tick(30)
        if player.game():
            score += 1
        else:
            base_speed = 0
            score += 0
            run = False
            save_records()
            game_over_sound.play()
            pygame.time.wait(2000)

pygame.quit()
