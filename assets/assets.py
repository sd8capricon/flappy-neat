import os
import pygame

BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "bird1.png")), (51,36)),
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))]
PIPE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pipe.png")), (78, 480))
BASE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "base.png")), (504, 168))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (432,768))
RESTART = pygame.image.load(os.path.join("assets", "restart.png"))