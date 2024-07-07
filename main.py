import neat.nn.feed_forward
import pygame
import neat
import random
from pygame.locals import *
from config import WIN_HEIGHT, WIN_WIDTH, WIN_SIZE
from game_state import FPS, GROUND_SCROLL, SCROLL_SPEED, GAME_OVER, LAST_PIPE, PIPE_FREQ, PASS_PIPE, SCORE
from assets import BASE_IMG, BG_IMG
from sprites import Bird, Pipe, Button
from typing import List


def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def eval_genomes(genomes, config):

    global GROUND_SCROLL, LAST_PIPE, SCORE

    # Window Setup
    DISPLAY_SURF = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    # Pipe States
    SCORE = 0
    LAST_PIPE = pygame.time.get_ticks() - PIPE_FREQ
    PASS_PIPE = False

    birds:List[Bird] = []
    birdScores:List[int] = []
    nets:List[neat.nn.FeedForwardNetwork] = []
    ge:List[neat.DefaultGenome] = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(100, int(WIN_HEIGHT/2)))
        ge.append(genome)

    pygame.init()
    running = True

    # font
    font = pygame.font.SysFont('Arial', 60)
    # defind color
    white = (255,255,255)

    # Sprite Groups
    pipe_group = pygame.sprite.Group()

    # Sprite Initialization
    birdy = Bird(100, int(WIN_HEIGHT/2))
    button = Button(WIN_WIDTH // 2 - 50, WIN_HEIGHT // 2 - 100)

    while running:
        
        # Lock Framerate
        clock.tick(FPS)

        # Set BG Image
        DISPLAY_SURF.blit(BG_IMG, (0,0))

        # Check Score
        if len(pipe_group)>0:
            if birdy.rect.left>pipe_group.sprites()[0].rect.left\
                and birdy.rect.right<pipe_group.sprites()[0].rect.right\
                and PASS_PIPE == False:
                PASS_PIPE = True
            if PASS_PIPE == True:
                if birdy.rect.left>pipe_group.sprites()[0].rect.right:
                    SCORE += 1
                    # Reward bird
                    PASS_PIPE = False
        
        # draw_text(str(score), font, white, int(WIN_WIDTH/2), 20)
        
        # Draw all Birds
        for bird in birds:
            bird.draw(DISPLAY_SURF)
        # Draw Pipe
        pipe_group.draw(DISPLAY_SURF)
        
        # Set Ground Base Image
        DISPLAY_SURF.blit(BASE_IMG, (GROUND_SCROLL, 600)) # 768-168

        # Check Collision
        # if pygame.sprite.spritecollide(birdy, pipe_group, False) or birdy.rect.top < 0:
        #     game_over = True
        for bird in birds:
            i = birds.index(bird)

            bird.update()

            if len(pipe_group)>0:
                top_pipe_cord = pipe_group.sprites()[0].rect.bottomleft[1]
                bottom_pipe_cord = pipe_group.sprites()[0].rect.topleft[1]
                # Reward for being alive
                ge[i].fitness += 0.5
                # Predict to jump or not
                prediction = nets[i].activate([bird.rect.y, top_pipe_cord, bottom_pipe_cord])
                if prediction[0]>0.5:
                    bird.jump()

            # Check Collision
            if pygame.sprite.spritecollide(bird, pipe_group, False) or bird.rect.top < 0:
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        # event loop
        if len(birds)>0:
            time_now = pygame.time.get_ticks()
            if time_now-LAST_PIPE>PIPE_FREQ:
                pipe_height = random.randint(-100,100)
                top_pipe = Pipe(WIN_WIDTH, int(WIN_HEIGHT/2)+pipe_height,1)
                btm_pipe = Pipe(WIN_WIDTH, int(WIN_HEIGHT/2)+pipe_height,-1)
                pipe_group.add(top_pipe) # Even Index -> Top
                pipe_group.add(btm_pipe) # Odd Index  -> Bottom
                LAST_PIPE = time_now

            # Update Birdy every frame
            # birdy.update()
            # Update Pipe every frame
            pipe_group.update()
            # Scroll Base
            GROUND_SCROLL -= SCROLL_SPEED
            # Reset Base Image Position
            if abs(GROUND_SCROLL)>(504-432):
                GROUND_SCROLL=0

        # Gameover
        for bird in birds:
            i = birds.index(bird)
            if bird.rect.bottom>=600:
                # game_over = True
                # birdy.flying = False
                bird.flying=False
                ge[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        #check for game over and reset
        # if game_over == True:
        #     if button.draw(DISPLAY_SURF):
        #         game_over = False
        #         score = reset_game()

        if len(birds)<=0:
            running=False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Number of birds alive", len(birds))
                running=False
                break
        pygame.display.update()
    pygame.quit()




config_file = "config.txt"

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

p = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(5))

winner = p.run(eval_genomes, 50)