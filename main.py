import neat.nn.feed_forward
import pygame
import neat
import random
import math
import pickle
from pygame.locals import *
from config import WIN_HEIGHT, WIN_WIDTH, WIN_SIZE
from game_state import FPS, GROUND_SCROLL, SCROLL_SPEED, LAST_PIPE, PIPE_FREQ, SCORE
from assets import BASE_IMG, BG_IMG
from sprites import Bird, Pipe, Button
from typing import List

generation = 0

def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def eval_genomes(genomes, config):

    global GROUND_SCROLL, LAST_PIPE, SCORE, generation

    # Window Setup
    DISPLAY_SURF = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    # Pipe States (reset every call)
    ITER_SCORE = 0
    LAST_PIPE = pygame.time.get_ticks() - PIPE_FREQ

    birds:List[Bird] = []
    birdScores:List[int] = []
    nets:List[neat.nn.FeedForwardNetwork] = []
    genomeList:List[neat.DefaultGenome] = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(100, int(WIN_HEIGHT/2)))
        birdScores.append(0)
        genomeList.append(genome)

    pygame.init()
    running = True

    # font
    font = pygame.font.SysFont('Arial', 32)
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

        
        # draw_text(str(score), font, white, int(WIN_WIDTH/2), 20)
        
        # Draw all Birds
        for bird in birds:
            bird.draw(DISPLAY_SURF)
        # Draw Pipe
        pipe_group.draw(DISPLAY_SURF)
        
        # Set Ground Base Image
        DISPLAY_SURF.blit(BASE_IMG, (GROUND_SCROLL, 600)) # 768-168

        # Check Collision
        for bird in birds:
            i = birds.index(bird)
            bird.update()
            if len(pipe_group)>0:
                top_pipe = pipe_group.sprites()[0]
                btm_pipe = pipe_group.sprites()[1]

                # Increment Bird Score
                if bird.rect.left>top_pipe.rect.left\
                    and bird.rect.right<top_pipe.rect.right\
                    and bird.pass_pipe == False:
                    bird.pass_pipe = True
                if bird.pass_pipe == True:
                    if bird.rect.left>top_pipe.rect.right:
                        bird.score += 1
                        # Reward bird for passing the pipes
                        genomeList[i].fitness += 5
                        bird.pass_pipe = False

                # Update max score
                if bird.score>ITER_SCORE:
                    ITER_SCORE = bird.score

                top_pipe_cord = top_pipe.rect.bottomleft[1]
                bottom_pipe_cord = btm_pipe.rect.topleft[1]
                gap_mid_x = top_pipe.rect.left
                gap_mid_y = abs(bottom_pipe_cord-top_pipe_cord)/2
                bird_pipe_dist = math.sqrt((bird.rect.x-gap_mid_x)**2+(bird.rect.y-gap_mid_y)**2)

                delta_x = abs(bird.rect.x-top_pipe.rect.x)
                delta_y_top = bird.rect.y-top_pipe.rect.bottom
                delta_y_bottom = bird.rect.y-btm_pipe.rect.top

                net_ip = (bird.vel, delta_x, delta_y_top, delta_y_bottom)

                # Reward for being alive
                genomeList[i].fitness += 0.1
                # Predict to jump or not
                prediction = nets[i].activate(net_ip)
                if prediction[0]>0.8:
                    bird.jump()

            # Check Collision
            if pygame.sprite.spritecollide(bird, pipe_group, False) or bird.rect.top < 0:
                genomeList[i].fitness -= 1
                birds.pop(i)
                nets.pop(i)
                genomeList.pop(i)

        # Draw Score
        # score = max(bird.score for bird in birds)
        draw_text("Gen: " + str(generation), font, white, 20, 20, DISPLAY_SURF)
        draw_text("Max: " + str(SCORE), font, white, 20, 60, DISPLAY_SURF)
        draw_text("Alive: " + str(len(birds)), font, white, 20, 100, DISPLAY_SURF)
        draw_text("Score: " + str(ITER_SCORE), font, white, 290, 20, DISPLAY_SURF)

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
                bird.flying=False
                genomeList[i].fitness -= 2
                birds.pop(i)
                nets.pop(i)
                genomeList.pop(i)

        if len(birds)<=0:
            running=False
            break

        for genome in genomeList:
            if genome.fitness>1000:
                running=False
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Number of birds alive", len(birds))
                running=False
                break
        pygame.display.update()
        
    generation += 1
    if ITER_SCORE>SCORE:
        SCORE=ITER_SCORE
    pygame.quit()


config_file = "config.txt"
def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10, filename_prefix="checkpoints/neat-checkpoint-"))

    winner = p.run(eval_genomes, 200)

    with open("winner/winner-genome", "wb") as f:
        pickle.dump(winner, f)
    
    with open("winner/stat.pkl", "wb") as f:
        pickle.dump(stats, f)

# run(config_file)