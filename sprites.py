# The file was created by: Matthew Doan

#Import libraries
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import sys

#Import Sprite Class
from pygame.sprite import Sprite

#New collision and movement interactions for opponent
vector = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

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

        #Changable parameters using objects
        self.speed = 300
        self.hitpoints = 20
        self.sword = False
        self.opponent_count = 6

        #Position and direction vectors for movement
        self.pos = vector(0,0)
        self.dir = vector(0,0)

    #Get input from keyboard to move player
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
            self.dir = (-1,0)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.dir = (1,0)
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
            self.dir = (0,-1)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.dir = (0,1)
        if self.vx != 0 and self.vy != 0: #diagonal physics
            self.vx *= 0.7071
            self.vy *= 0.7071
    
    #Player collision with walls
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
                self.speed += 100
            if str(object_collision[0].__class__.__name__) == "Hitpoints":
                self.hitpoints += 10
            if str(object_collision[0].__class__.__name__) == "Sword":
                self.sword = True
                self.collide_with_opponent_with_sword(self.game.Opponent, True)
    
    #Opponent collision interactions
    def collide_with_opponent(self, group, kill):
        opponent_collision = pg.sprite.spritecollide(self, group, False)
        if opponent_collision and self.sword == False:
            if str(opponent_collision[0].__class__.__name__) == "Opponent":
                self.hitpoints -= 1
        else:
         self.collide_with_opponent_with_sword(self.game.Opponent, True)
    
    #Sword interaction with opponents
    def collide_with_opponent_with_sword(self, group, kill):
        opponent_collision = pg.sprite.spritecollide(self, group, True)
        if opponent_collision and self.sword == True:
            if str(opponent_collision[0].__class__.__name__) == "Opponent":
                self.opponent_count -= 1
                

                
    #Update player movement
    #Update collision with objects
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')

        self.collide_with_group(self.game.Speed_PowerUP, True)
        self.collide_with_group(self.game.Hitpoints, True)
        self.collide_with_group(self.game.Sword, True)
        self.collide_with_opponent(self.game.Opponent, False)

#Wall class
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
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
        self.image = self.game.Speed_PowerUP_img
        self.rect = self.image.get_rect()
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
        self.image = self.game.Hitpoints_img
        self.rect = self.image.get_rect()
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
        self.image = self.game.opponent_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        #New opponent movement
        self.pos = vector(x, y) * TILESIZE
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 250
        
        self.speed = 300
        self.chasing = False
        
    #New opponent chasing
    #Citation: Mr. Cozort's game engine github
    #Change: Changed Chasing chase_distance and speed of opponent chasing
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    
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
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vector(1, 0))
            self.rect.center = self.pos
            self.acc = vector(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            collide_with_walls(self, self.game.walls, 'x')
            collide_with_walls(self, self.game.walls, 'y')
#Sword class
class Sword(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Sword
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.Sword_img
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE 
