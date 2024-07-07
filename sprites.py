from typing import Any
import pygame
from game_state import SCROLL_SPEED, PIPE_GAP
from assets import BIRD_IMGS, PIPE_IMG, RESTART

class Sprite(pygame.sprite.Sprite):
    def __init__(self, IMG:pygame.Surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMG
        self.rect = IMG.get_rect()
    
    def draw(self, screen:pygame.Surface):
        screen.blit(self.image, self.rect)


class Bird(Sprite):
    src = BIRD_IMGS[0]
    pass_pipe = False
    score = 0
    vel = 0
    flying = True
    clicked = False

    def __init__(self, x, y):
        super().__init__(self.src, x, y)
        self.rect.center = [x,y]

    def jump(self):
        # jump
        self.vel-=5

    def update(self):
        if self.flying:
            self.vel += 0.5
            # Cap Velocity
            if self.vel > 8:
                self.vel = 8
            # Gravity
            if self.rect.bottom < 600:
                self.rect.y += int(self.vel)

        # jump
        if pygame.mouse.get_pressed()[0]==1 and self.clicked==False and self.rect.y>-5:
            self.clicked=True
            self.vel = -10
        if pygame.mouse.get_pressed()[0]==0 and self.clicked==True:
            self.clicked=False

        # Rotate Bird while falling
        self.image = pygame.transform.rotate(self.src.copy(), self.vel*-2)


class Pipe(Sprite):
    src = PIPE_IMG

    def __init__(self, x, y, position):
        super().__init__(self.src, x, y)

        # position 1 from top position -1 from bottom
        # Min, Max bottom pipe y = [0, 600] [pipe at top, pipe at bottom]
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y-int(PIPE_GAP/2)]
        if position == -1:
            self.rect.topleft = [x,y+int(PIPE_GAP/2)]

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right<0:
            self.kill()

class Button():
    src = RESTART
	
    def __init__(self, x, y):
        self.image = self.src
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen:pygame.Surface):
        action = False

		#get mouse position
        pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

		#draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action