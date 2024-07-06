import pygame

fps = 60

game_over = False
ground_scroll = 0
scroll_speed = 4
score = 0

pipe_gap = 150
pipe_freq = 1500 # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq

pass_pipe = False