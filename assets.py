import os
import pygame

BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird1.png")), (51,36)),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "pipe.png")), (78, 480))
BASE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "base.png")), (504, 168))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")), (432,768))
RESTART = pygame.image.load(os.path.join("imgs", "restart.png"))