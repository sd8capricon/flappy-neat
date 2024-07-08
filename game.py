import neat
import pygame
import random
from pygame.locals import *
from config.config import WIN_HEIGHT, WIN_WIDTH, WIN_SIZE
from config.game_state import FPS, GROUND_SCROLL, SCROLL_SPEED, GAME_OVER, LAST_PIPE, PIPE_FREQ
from assets.assets import BASE_IMG, BG_IMG
from sprites.sprites import Bird, Pipe, Button
from utils.utils import draw_text


def reset_game(pipe_group, birdy: Bird):
    pipe_group.empty()
    birdy.rect.x = 100
    birdy.rect.y = int(WIN_HEIGHT / 2)
    score = 0
    return score


def play(genome: neat.DefaultGenome = None, config: neat.Config = None):

    global GROUND_SCROLL, GAME_OVER, LAST_PIPE
    DISPLAY_SURF = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    running = True

    # font
    font = pygame.font.SysFont('Arial', 60)
    # defind color
    white = (255, 255, 255)

    # Sprite Groups
    pipe_group = pygame.sprite.Group()

    # Sprite Initialization
    birdy = Bird(100, int(WIN_HEIGHT/2))
    button = Button(WIN_WIDTH // 2 - 50, WIN_HEIGHT // 2 - 100)

    if genome:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

    while running:

        # Lock Framerate
        clock.tick(FPS)

        # Set BG Image
        DISPLAY_SURF.blit(BG_IMG, (0, 0))

        # Check Score
        if len(pipe_group) > 0:
            if birdy.rect.left > pipe_group.sprites()[0].rect.left\
                    and birdy.rect.right < pipe_group.sprites()[0].rect.right\
                    and birdy.pass_pipe == False:
                birdy.pass_pipe = True
            if birdy.pass_pipe == True:
                if birdy.rect.left > pipe_group.sprites()[0].rect.right:
                    birdy.score += 1
                    birdy.pass_pipe = False

            if genome:
                top_pipe = pipe_group.sprites()[0]
                btm_pipe = pipe_group.sprites()[1]
                delta_x = abs(birdy.rect.x-top_pipe.rect.x)
                delta_y_top = birdy.rect.y-top_pipe.rect.bottom
                delta_y_bottom = birdy.rect.y-btm_pipe.rect.top
                net_ip = (birdy.vel, delta_x, delta_y_top, delta_y_bottom)

                prediction = net.activate(net_ip)
                if prediction[0] > 0.8:
                    birdy.jump()

        # Draw Bird
        birdy.draw(DISPLAY_SURF)
        # Draw Pipe
        pipe_group.draw(DISPLAY_SURF)
        # Draw Score
        draw_text(str(birdy.score), font, white,
                  int(WIN_WIDTH/2), 20, DISPLAY_SURF)

        # Set Ground Base Image
        DISPLAY_SURF.blit(BASE_IMG, (GROUND_SCROLL, 600))  # 768-168

        # Check Collision
        if pygame.sprite.spritecollide(birdy, pipe_group, False) or birdy.rect.top < 0:
            GAME_OVER = True

        if GAME_OVER == False and birdy.flying == True:
            time_now = pygame.time.get_ticks()
            if time_now-LAST_PIPE > PIPE_FREQ:
                pipe_height = random.randint(-100, 100)
                top_pipe = Pipe(WIN_WIDTH, int(WIN_HEIGHT/2)+pipe_height, 1)
                btm_pipe = Pipe(WIN_WIDTH, int(WIN_HEIGHT/2)+pipe_height, -1)
                pipe_group.add(top_pipe)
                pipe_group.add(btm_pipe)
                LAST_PIPE = time_now

            # Update Birdy every frame
            birdy.update()
            # Update Pipe every frame
            pipe_group.update()
            # Scroll Base
            GROUND_SCROLL -= SCROLL_SPEED
            # Reset Base Image Position
            if abs(GROUND_SCROLL) > (504-432):
                GROUND_SCROLL = 0

        # Gameover
        if birdy.rect.bottom >= 600:
            GAME_OVER = True
            birdy.flying = False

        # check for game over and reset
        if GAME_OVER == True:
            if button.draw(DISPLAY_SURF):
                GAME_OVER = False
                birdy.score = reset_game(pipe_group, birdy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and birdy.flying == False:
                birdy.flying = True
        pygame.display.update()
    pygame.quit()
