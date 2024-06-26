# The file was created by: Matthew Doan

#Import libraries
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import sys
from os import path
import random

#Import Sprite Class
from pygame.sprite import Sprite

#New collision and movement interactions for opponent
vector = pg.math.Vector2

#animated sprite png file
SPRITESHEET = "theBell.png"

#define image folder
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

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

#Get image
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
    
#Player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups) 
        self.game = game

        #Load image to player
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()

        #Stages of animated sprite
        self.jumping = False
        self.walking = False
        self.current_frame = 0
        self.last_update = 0

        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        #Changable parameters using objects
        self.speed = 300
        self.hitpoints = 20
        self.sword = False
        self.opponent_count = 4

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
            if str(object_collision[0].__class__.__name__) == "Invisible_Slowness_Tiles": #Final Design Goal
                self.speed -= 50
                self.display_jumpscares()
    
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
                print(self.opponent_count)

    #Load sprites on player            
    def load_images(self):
            self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                    self.spritesheet.get_image(32,0, 32, 32)]
            # for frame in self.standing_frames:
            #     frame.set_colorkey(BLACK)

    #Display jumpscare images
    #Final design goal 
    def display_jumpscares(self):

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BLACK)
        
        self.jumpscare = random.choice(self.game.jumpscare_images)

        #Citation: ChatGPT
        self.jumpscare_rect = self.jumpscare.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(self.jumpscare, self.jumpscare_rect)
        self.game.jumpscare_sound.play()    
        pg.display.flip()
        pg.time.delay(2000)
        

    #Animate sprite
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    

    #Update player movement
    #Update collision with objects
    def update(self):
        #Calls animate functon
        self.animate()
        
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
        self.collide_with_group(self.game.Invisible_Slowness_Tiles, True)
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
        self.chase_distance = 100
        
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
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.Sword_img
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE 

#Jump scare Tile Class
#Final Design Goal
class Invisible_Slowness_Tiles(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Invisible_Slowness_Tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BGCOLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
