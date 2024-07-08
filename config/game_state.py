import pygame

FPS = 60

GAME_OVER = False
GROUND_SCROLL = 0
SCROLL_SPEED = 4
SCORE = 0

PIPE_GAP = 150
PIPE_FREQ = 1500  # milliseconds
LAST_PIPE = pygame.time.get_ticks() - PIPE_FREQ
PASS_PIPE = False
