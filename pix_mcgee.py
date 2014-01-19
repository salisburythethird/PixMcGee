#!/usr/bin/python
"""
|\ --- \  /
|/  |   \/
|   |   /\
|  _|_ /  \
MCGEE
"""
#Made by Tin Can Games

import pygame as pg
import os
import sys
WIDTH = 800
HEIGHT = 600
BLACK = ( 0, 0, 0 )
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
D_GRAY = (50, 50, 50)
L_GRAY = (150, 150, 150)
GREEN = (20, 125, 20)


class Entity(pg.sprite.DirtySprite):

    def __init__(self):
        pg.sprite.DirtySprite.__init__(self)


class Player(Entity):
    """ Makes a Playable Sprite """
    change_x = 4
    change_y = 4
    
    def __init__(self):
        """ Creates the Player """
        Entity.__init__(self)
        self.images = []
        for i in range(1, 5):
            img = pg.image.load("pix" + str(i) + ".png").convert()
            img.set_colorkey(WHITE)
            self.images.append(img)
##        for i in range(1, 5):
##            img = pg.Surface((20,20))
##            img = img.convert()
##            img.fill(WHITE)
##            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.surface = pg.Surface((self.rect.width, self.rect.height))
            
    def update(self, keys_pressed, block_list):
        self.dirty = 0
        if keys_pressed[pg.K_LEFT]:
            self.image = self.images[3]
            tmp_rect = self.rect
            self.rect = self.image.get_rect()
            self.rect.x = tmp_rect.x
            self.rect.y = tmp_rect.y
            self.move(-self.change_x, 0, block_list)
            
        if keys_pressed[pg.K_RIGHT]:
            self.image = self.images[1]
            tmp_rect = self.rect
            self.rect = self.image.get_rect()
            self.rect.x = tmp_rect.x
            self.rect.y = tmp_rect.y
            self.move(self.change_x, 0, block_list)
            
        if keys_pressed[pg.K_UP]:
            self.image = self.images[0]
            tmp_rect = self.rect
            self.rect = self.image.get_rect()
            self.rect.x = tmp_rect.x
            self.rect.y = tmp_rect.y
            self.move(0, -self.change_y, block_list)
            
        if keys_pressed[pg.K_DOWN]:
            self.image = self.images[2]
            tmp_rect = self.rect
            self.rect = self.image.get_rect()
            self.rect.x = tmp_rect.x
            self.rect.y = tmp_rect.y
            self.move(0, self.change_y, block_list)

    def move(self, dx, dy, barriers):
        if dx != 0:
            self.move_single_axis(dx, 0, barriers)
            self.dirty = 1
        if dy != 0:
            self.move_single_axis(0, dy, barriers)
            self.dirty = 1

    def move_single_axis(self, dx, dy, barriers):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a barrier, move out based on velocity
        for b in barriers:
            if self.rect.colliderect(b.rect):
                if dx > 0: # Moving right; Hit the left side of the barrier
                    self.rect.right = b.rect.left
                if dx < 0: # Moving left; Hit the right side of the barrier
                    self.rect.left = b.rect.right
                if dy > 0: # Moving down; Hit the top side of the barrier
                    self.rect.bottom = b.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the barrier
                    self.rect.top = b.rect.bottom

        
class Road(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.convert()
        self.image.fill(D_GRAY)
        self.rect = pg.Rect(x, y, 20, 20)
        

class Sidewalk(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.convert()
        self.image.fill(L_GRAY)
        self.rect = pg.Rect(x, y, 20, 20)
        self.dirty = 0

        
def draw_level(all_sprites_group, sidewalk_group):

    x = y = 0
    level = [
    "     SRRRRRS             SRRRRRS        ",
    "     SRRRRRS             SRRRRRS        ",
    "     SRRRRRS             SRRRRRS        ",
    "     SRRRRRS             SRRRRRS        ",
    "     SRRRRRS             SRRRRRS        ",
    "     SRRRRRSSSSSSSSSSSSSSSRRRRRS        "
    "     SRRRRRRRRRRRRRRRRRRRRRRRRRS        ",
    "     SRRRRRRRRRRRRRRRRRRRRRRRRRS        ",
    "     SRRRRRRRRRRRRRRRRRRRRRRRRRS        ",
    "     SRRRRRRRRRRRRRRRRRRRRRRRRRS        ",
    "     SRRRRRRRRRRRRRRRRRRRRRRRRRS        ",
    "     SSSSSSSSSSSRRRRRSSSSSSSSSSS        ",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "SSSSSSSSSSSSSSSSRRRRRSSSSSSSSSSSSSSSSSSS",
    "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",
    "SSSSSSSSSSSSSSSSRRRRRSSSSSSSSSSSSSSSSSSS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS",
    "               SRRRRRS"
    ]

    for row in level:
        for col in row:
            if col == "R":
                r = Road(x, y)
                all_sprites_group.add(r)
            if col == "S":
                s = Sidewalk(x, y)
                sidewalk_group.add(s)
                all_sprites_group.add(s)
            x += 20
        y += 20
        x = 0



def main():
    # Initialize Pygame
    pg.init()
    # Set mode for screen
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Pix McGee")

    # create a background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREEN)


    screen.blit(background,(0,0))
    pg.display.flip()

    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
    clock = pg.time.Clock()
    done = False

    # Make a group
    all_sprites_list = pg.sprite.LayeredDirty()
    sidewalk_sprites = pg.sprite.LayeredDirty()
    draw_level(all_sprites_list, sidewalk_sprites)
    player = Player()
    # hard-coded position. we need to make this dynamic
    player.rect.x = 120 # road and sidewalk sprites are 20 pixels wide. 6 *20
    
    all_sprites_list.add(player)
    pg.key.set_repeat(5, 0)



    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                player.update( pg.key.get_pressed(), sidewalk_sprites )
                if event.key == pg.K_ESCAPE:
                    done = True

        clock.tick(60)
        #screen.fill(GREEN)
        
        rects = all_sprites_list.draw(screen)
        pg.display.update(rects)

    pg.quit()
    
if __name__ == '__main__':
    main()
