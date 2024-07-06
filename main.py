import pygame
import random
from pygame.locals import *
from config import WIN_HEIGHT, WIN_WIDTH, WIN_SIZE
from game_state import fps, ground_scroll, scroll_speed, game_over, last_pipe, pipe_freq, pass_pipe, score
from assets import BASE_IMG, BG_IMG
from sprites import Bird, Pipe, Button

DISPLAY_SURF = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    DISPLAY_SURF.blit(img, (x,y))

def reset_game():
	pipe_group.empty()
	birdy.rect.x = 100
	birdy.rect.y = int(WIN_HEIGHT / 2)
	score = 0
	return score

if __name__ == "__main__":
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
        clock.tick(fps)

        # Set BG Image
        DISPLAY_SURF.blit(BG_IMG, (0,0))

        # Check Score
        if len(pipe_group)>0:
            if birdy.rect.left>pipe_group.sprites()[0].rect.left\
                and birdy.rect.right<pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if birdy.rect.left>pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False
        
        draw_text(str(score), font, white, int(WIN_WIDTH/2), 20)
        
        # Draw Bird
        birdy.draw(DISPLAY_SURF)
        # Draw Pipe
        pipe_group.draw(DISPLAY_SURF)
        
        # Set Ground Base Image
        DISPLAY_SURF.blit(BASE_IMG, (ground_scroll, 600)) # 768-168

        # Check Collision
        if pygame.sprite.spritecollide(birdy, pipe_group, False) or birdy.rect.top < 0:
            game_over = True

        if game_over == False and birdy.flying==True:
            time_now = pygame.time.get_ticks()
            if time_now-last_pipe>pipe_freq:
                pipe_height = random.randint(-100,100)
                top_pipe = Pipe(WIN_WIDTH, int(WIN_HEIGHT/2)+pipe_height,1)
                btm_pipe = Pipe(WIN_WIDTH, int(WIN_HEIGHT/2)+pipe_height,-1)
                pipe_group.add(top_pipe)
                pipe_group.add(btm_pipe)
                last_pipe = time_now

            # Update Birdy every frame
            birdy.update()
            # Update Pipe every frame
            pipe_group.update()
            # Scroll Base
            ground_scroll -= scroll_speed
            # Reset Base Image Position
            if abs(ground_scroll)>(504-432):
                ground_scroll=0

        # Gameover
        if birdy.rect.bottom>=600:
            game_over = True
            birdy.flying = False

        #check for game over and reset
        if game_over == True:
            if button.draw(DISPLAY_SURF):
                game_over = False
                score = reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN and birdy.flying==False:
                birdy.flying = True
        pygame.display.update()
    pygame.quit()