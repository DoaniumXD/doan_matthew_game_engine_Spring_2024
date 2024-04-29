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

#1 Design Goal (Beta Version):
# Goal: Add in a pause screen and add background music that stops when pause screen is shown

#3 Design Goals (Alpha Version): 
#1. Add timer in game
#2. Multiple screens for winning, dying, running out of time, and for the start
#3. Collectable Weapons to kill enemies

# Game design truths:
# Goals: Kill all opponents by collecting the sword and without dying in 35 seconds to win
# Rules: Must stay within the box and can't go through walls; Game ends if health or time or number of enemies go to 0
# Feedback: Collision with enemies cause health to go down; Powerups give certain effects and disappear; Sword makes enemies disapper
# Freedom: Able to move in the x and y direction. Able to collect, interact, and collide with objects.


#Cooldown Class to set in game timer
#Citation: Mr. Cozort's game engine github
#Change: Made timer countdown instead of counting up
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
    
    #reset event timer
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    
    #set current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
    
#Game class 
class Game:

    #Initialize Method --> Intializes Game Class
    def __init__(self):
        #Init pygame
        pg.init()
        pg.mixer.init() 

        #Set title and define screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        #setting game clock
        self.clock = pg.time.Clock()

        self.load_data()

        #Pause game variables
        self.running = True
        self.paused = False

    #Load save game data
    #Added images folder and image in the load_data method for use with the player and objects
    def load_data(self):
        game_folder = path.dirname(__file__)

        self.img_folder = path.join(game_folder, 'images') #Define images folder
        self.snd_folder = path.join(game_folder, 'sounds') #Define sounds folder
        #self.player_img = pg.image.load(path.join(self.img_folder, 'OSHAWOTT.png')).convert_alpha()
        self.opponent_img = pg.image.load(path.join(self.img_folder, 'PIKACHU.png')).convert_alpha()
        self.Speed_PowerUP_img = pg.image.load(path.join(self.img_folder, 'Speed_PowerUP.png')).convert_alpha()
        self.Hitpoints_img = pg.image.load(path.join(self.img_folder, 'HEART.png')).convert_alpha()
        self.Sword_img = pg.image.load(path.join(self.img_folder, 'SWORD.png')).convert_alpha()

        #Load map data for player and objects
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    
    # Init all variables, setup groups, instantiate classes
    def new(self):
        #Load music file from sounds folder
        pg.mixer.music.load(path.join(self.snd_folder,'Megalovania.mp3'))

        self.test_timer = Cooldown()
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
        #Play music forever when game is being played
        pg.mixer.music.play()
        self.playing = True
        while self.playing and self.waiting == False:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
       
        
    
    #Quit game and close window
    def quit(self):
         pg.quit()
         sys.exit()
    
    #Update all sprite groups
    #Update timer
    #Call display screen functions when health, time, and opponent count update
    #Able to stop timer and sprite movement with pause
    def update(self):
         if not self.paused:
            self.test_timer.ticking()
            self.all_sprites.update()
            #Beta Project Design Goal
            pg.mixer.music.unpause() #Play music if game is playing

         if self.test_timer.countdown(35) < 0:
             self.display_timeout_screen()
         if self.player.hitpoints == 0:
             self.display_death_screen()
         if self.player.opponent_count == 0:
             self.display_victory_screen()
        #Beta Project Design Goal
         if self.paused:
             self.display_pause_screen()
             pg.mixer.music.pause() #Stop playing music if game is paused
        

    #Draw lines to make grid
    #def draw_grid(self):
    #    for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
    #    for y in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))
    
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
        #self.draw_grid()
        self.all_sprites.draw(self.screen) 
        self.draw_text(self.screen, "Time Remaining: ", 48, WHITE, 1, 2)
        self.draw_text(self.screen, str(self.test_timer.countdown(35)), 48, WHITE, 10.5, 2)
        self.draw_text(self.screen, "Health: ", 48, WHITE, 1, 0.75)
        self.draw_text(self.screen, str(self.player.hitpoints), 48, WHITE, 5, 0.75)
        pg.display.flip()
        

    #Define Input Method and get input from keyboard
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
        
        #Take in input to pause game
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            if not self.paused:
                self.paused = True
            else:
                self.paused = False

    #Display start screen with instructions
    def display_start_screen(self):
            self.screen.fill(PINK)
            self.draw_text(self.screen, "Find the sword and kill all the mobs to win!", 24, WHITE, 10.25, 3)
            self.draw_text(self.screen, "Press the space bar to start!", 24, WHITE, 12, 6)
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
    #Display victory screen
    def display_victory_screen(self):
        self.screen.fill(GREEN)
        self.draw_text(self.screen, "YOU WIN!", 64, WHITE, 12, 3)
        pg.display.flip()
        self.wait_for_key()
    
    #Display pause screen
    #Beta Project Design Goal
    def display_pause_screen(self):
        self.screen.fill(PINK)
        self.draw_text(self.screen, "You have paused the game. Press the space bar to resume", 24, WHITE, 8, 6)
        pg.display.flip()
        self.wait_for_key()

    #Press space bar to start game or to pause the game
    def wait_for_key(self):
            self.waiting = True
                   
            while self.waiting:
                self.clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.waiting = False
                        self.quit()

                keys = pg.key.get_pressed()
                if keys[pg.K_SPACE]:
                        self.waiting = False

#Citation: Mr. Cozort's game engine github
#Change: Added more display screens and called them when certain requirements are met
    


#Instantiation of the Game class    
g = Game()

#Call display start screen function
g.display_start_screen()

while True:
     g.new()
     g.run()
     

#Run game
g.run()

        
