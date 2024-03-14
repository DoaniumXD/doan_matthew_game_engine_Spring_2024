#The file was created by: Matthew Doan
#My first source control edit
#importing libraries
import pygame as pg
import sys 
from settings import *
from sprites import * 
from os import path
from time import sleep
from math import floor

# 3 Features I am committed to adding and haven't added yet: 
    #1. Enemies with collisons and health bar interactions
    #2. Multiple screens for winning, dying, running out of time, and for the start
    #3. Collectable Weapons to kill enemies


#Cooldown Class
class Cooldown():
    #set all properties to 0 when instantiated
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        self.cd = 0
    
    #Use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    
    def get_cd(self):
        return self.cd
    #resets event time to 0/reset cooldown
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            self.cd = x
            return x
    
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    
    #set current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
    
#Game class 
class Game:

    #Initialize Method --> Intializes Game Class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        #setting game clock
        self.clock = pg.time.Clock()
        #pg.key.set_repeat(500, 100)
        self.load_data()

    #Load save game data
    #Added images folder and image in the load_data method for use with the player
    def load_data(self):
        game_folder = path.dirname(__file__)
        
        self.img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, 'OSHAWOTT.png')).convert_alpha()
        self.opponent_img = pg.image.load(path.join(self.img_folder, 'PIKACHU.png')).convert_alpha()
        self.Speed_PowerUP_img = pg.image.load(path.join(self.img_folder, 'Speed_PowerUP.png')).convert_alpha()
        self.Hitpoints_img = pg.image.load(path.join(self.img_folder, 'HEART.png')).convert_alpha()
        self.Sword_img = pg.image.load(path.join(self.img_folder, 'SWORD.png')).convert_alpha()

        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    
    # Init all variables, setup groups, instantiate classes
    def new(self):
        self.test_timer = Cooldown()
        self.power_up_cooldown = Cooldown()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.Speed_PowerUP = pg.sprite.Group()
        self.Hitpoints = pg.sprite.Group()
        self.Break_Walls_PowerUP = pg.sprite.Group()
        self.Opponent = pg.sprite.Group()
        self.Sword = pg.sprite.Group()
    
        for row, tiles in enumerate(self.map_data):
            print(self.map_data)
            for col, tile in enumerate(tiles):
                #Uses a string to denote an instance of a game object
                if tile == '1':
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "S":
                    Speed_PowerUP(self, col, row)
                if tile == "H":
                    Hitpoints(self, col, row)
                if tile == "O":
                    Opponent(self, col, row)
                if tile == "W":
                    Sword(self, col, row)
    
                    
    #Define Run Method in Game Engine
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    #Quit game and close window
    def quit(self):
         pg.quit()
         sys.exit()
    
    #Update all sprite groups
    def update(self):
         self.test_timer.ticking()
         self.all_sprites.update()
         if self.test_timer.countdown(63) < 0:
             self.display_timeout_screen()
         if self.player.hitpoints == 0:
             self.display_death_screen()
        

    #Draw lines to make grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
             pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
             pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))
    
    #Display text on screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    
    #Draw grid, fill in BG, Draw text, Display timer
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen) 
        self.draw_text(self.screen, "Time Remaining: ", 48, WHITE, 1, 2)
        self.draw_text(self.screen, str(self.test_timer.countdown(63)), 48, WHITE, 10.5, 2)
        self.draw_text(self.screen, "Health: ", 48, WHITE, 1, 0.75)
        self.draw_text(self.screen, str(self.player.hitpoints), 48, WHITE, 5, 0.75)
        pg.display.flip()
        

    #Define Input Method and get input from keyboard
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
           # if event.type == pg.KEYDOWN:
           #     if event.key == pg.K_LEFT:
           #         self.player.move(dx = -1)
           #     if event.key == pg.K_RIGHT:
           #          self.player.move(dx = 1)
           #     if event.key == pg.K_DOWN:
           #         self.player.move(dy = 1)
           #     if event.key == pg.K_UP:
           #          self.player.move(dy = -1)

    #Display start screen
    def display_start_screen(self):
            self.screen.fill(PINK)
            self.draw_text(self.screen, "Find the sword and kill all the mobs to win!", 24, WHITE, 10.5, 3)
            self.draw_text(self.screen, "Press any key to start!", 24, WHITE, 13, 6)
            pg.display.flip()
            self.wait_for_key()
    
    #Display timeout screen
    def display_timeout_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "You ran out of time! Try again!", 24, WHITE, 11.5, 3)
        pg.display.flip()
        self.wait_for_key()
    
    #Display death screen
    def display_death_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "YOU DIED!", 64, WHITE, 12, 3)
        pg.display.flip()
        self.wait_for_key()
    
    def display_victory_screen(self):
        pass
        self.screen.fill(YELLOW)
        self.draw_text(self.screen, "YOU WIN!", 64, WHITE, 12.5, 3)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
            waiting = True
            while waiting:
                self.clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        self.quit()
                    if event.type == pg.KEYUP:
                        waiting = False
    


#Instantiation of the Game class    
g = Game()

#Call display start screen function
g.display_start_screen()

while True:
     g.new()
     g.run()
     

#Run game
g.run()

        
