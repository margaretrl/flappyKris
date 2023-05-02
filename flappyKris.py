import pygame, random, time
from pygame.locals import *

# Global variables
speed = 20
fall = 2.5
game_speed = 15

window_w = 400
window_h = 600

ground_w = 2 * window_w
ground_h = 100

pipe_w = 110
pipe_h = 500
pipe_gap = 150


pygame.mixer.init()


class Kris(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.pts = 0

        self.images = [
            pygame.image.load("assets/sprites/kris-flap1.png").convert_alpha(),
            pygame.image.load("assets/sprites/kris-flap2.png").convert_alpha(),
            pygame.image.load("assets/sprites/kris-flap3.png").convert_alpha(),
        ]
        self.score_imgs = [
            pygame.image.load("assets/sprites/0.png").convert_alpha(),
            pygame.image.load("assets/sprites/1.png").convert_alpha(),
            pygame.image.load("assets/sprites/2.png").convert_alpha(),
            pygame.image.load("assets/sprites/3.png").convert_alpha(),
            pygame.image.load("assets/sprites/4.png").convert_alpha(),
            pygame.image.load("assets/sprites/5.png").convert_alpha(),
            pygame.image.load("assets/sprites/6.png").convert_alpha(),
            pygame.image.load("assets/sprites/7.png").convert_alpha(),
            pygame.image.load("assets/sprites/8.png").convert_alpha(),
            pygame.image.load("assets/sprites/9.png").convert_alpha(),
        ]

        self.current_image = 0
        self.image = pygame.image.load("assets/sprites/kris-flap1.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = window_w / 6
        self.rect[1] = window_h / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += fall
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -speed

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

    def add_pt(self):
        self.pts += 1


class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, x, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/sprites/martini.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (pipe_w, pipe_h))

        self.rect = self.image.get_rect()
        self.rect[0] = x

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = window_h - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= game_speed


class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (ground_w, ground_h))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = window_h - ground_h

    def update(self):
        self.rect[0] -= game_speed


# def set_bkground():
#     background = pygame.image.load("assets/sprites/background-hollywood.png")
#     background = pygame.transform.scale(background, (window_w, window_h))
#     init_msg = pygame.image.load("assets/sprites/message.png").convert_alpha()
#     return background, init_msg


def display_score(screen, score_imgs, score):
    score_digits = [int(d) for d in str(score)]
    total_width = 0

    for digit in score_digits:
        total_width += score_imgs[digit].get_width()

    x_offset = (window_w - total_width) / 2

    for digit in score_digits:
        screen.blit(score_imgs[digit], (x_offset, window_h * 0.1))
        x_offset += score_imgs[digit].get_width()


def get_random_pipes(x):
    size = random.randint(100, 300)
    pipe = Pipe(False, x, size)
    pipe_inverted = Pipe(True, x, window_h - size - pipe_gap)
    return pipe, pipe_inverted


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((window_w, window_h))
    pygame.display.set_caption("Flappy Kris")

    background = pygame.image.load("assets/sprites/background-hollywood.png")
    background = pygame.transform.scale(background, (window_w, window_h))
    init_img = pygame.image.load("assets/sprites/message.png").convert_alpha()

    bird_group = pygame.sprite.Group()
    bird = Kris()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()

    for i in range(2):
        ground = Ground(ground_w * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range(2):
        pipes = get_random_pipes(window_w * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

        pygame.mixer.music.load("assets/audio/hey-bestie.wav")
        pygame.mixer.music.play()

    clock = pygame.time.Clock()

    begin = True

    while begin:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bird.bump()
                    pygame.mixer.music.load("assets/audio/wing.wav")
                    pygame.mixer.music.play()
                begin = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load("assets/audio/wing.wav")
                    pygame.mixer.music.play()
                    begin = False

        screen.blit(background, (0, 0))
        screen.blit(init_img, (120, 150))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(ground_w - 20)
            ground_group.add(new_ground)

        bird.begin()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

    while True:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bird.bump()
                    pygame.mixer.music.load("assets/audio/wing.wav")
                    pygame.mixer.music.play()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load("assets/audio/wing.wav")
                    pygame.mixer.music.play()

        screen.blit(background, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(ground_w - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(window_w * 2)

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        if pygame.sprite.groupcollide(
            bird_group, ground_group, False, False, pygame.sprite.collide_mask
        ) or pygame.sprite.groupcollide(
            bird_group, pipe_group, False, False, pygame.sprite.collide_mask
        ):
            # display_score(screen, bird.score_imgs, bird.pts)
            # pygame.display.update()
            pygame.mixer.music.load("assets/audio/amazing.wav")
            pygame.mixer.music.play()
            time.sleep(5)
            break
        # else:
        #     bird.add_pt()
        #     print(bird.pts)
