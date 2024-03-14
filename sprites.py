# The file was created by: Matthew Doan

#Import libraries
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import sys

#Import Sprite Class
from pygame.sprite import Sprite

#Player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups) 
        self.game = game
        #added player image to sprite from game class
        self.image = game.player_img
        self.rect = self.image.get_rect()
        
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        self.hitpoints = 100
        
    #Get input from keyboard to move player
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0: #diagonal physics
            self.vx *= 0.7071
            self.vy *= 0.7071
    
    #Wall Collision interactions
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y
    
    #Object collision interactions
    def collide_with_group(self, group, kill):
        object_collision = pg.sprite.spritecollide(self, group, True)
        if object_collision:
            if str(object_collision[0].__class__.__name__) == "Speed_PowerUP":
                self.speed += 300
            if str(object_collision[0].__class__.__name__) == "Hitpoints":
                self.hitpoints += 50
            if str(object_collision[0].__class__.__name__) == "Opponent":
                self.hitpoints -= 1
            if str(object_collision[0].__class__.__name__) == "Sword":
                print("You got a sword! Kill the opponents!")
    
    #Opponent collision interactions
    def collide_with_opponent(self, group, kill):
        opponent_collision = pg.sprite.spritecollide(self, group, False)
        if opponent_collision:
            if str(opponent_collision[0].__class__.__name__) == "Opponent":
                self.hitpoints -= 1
                
    #Update player movement
    def update(self):
        #self.rect.x = self.x * TILESIZE 
        #self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_walls('x')
        self.collide_with_walls('y')

        self.collide_with_group(self.game.Speed_PowerUP, True)
        self.collide_with_group(self.game.Hitpoints, True)
        self.collide_with_group(self.game.Sword, True)
        self.collide_with_opponent(self.game.Opponent, False)

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

#Speed Power Up class
class Speed_PowerUP(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Speed_PowerUP 
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE 

#Hitpoints Class
class Hitpoints(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Hitpoints 
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE 

#Opponent Class
class Opponent(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Opponent
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    
    #Opponent wall collision interaction 
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    #Update opponent movement            
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

#Sword class
class Sword(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Sword
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE 
