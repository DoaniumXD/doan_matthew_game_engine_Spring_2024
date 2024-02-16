#The file was created by: Matthew Doan

#importing libraries
import pygame as pg
import sys 
from settings import *
from sprites import * 
from os import path
from time import sleep

#Game class 
class Game:

    #Initialize Method --> Intializes Game Class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    #Load save game data
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    
    # Init all variables, setup groups, instantiate classes
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.spike = pg.sprite.Group()
        #self.player = Player(self, 10, 10)
        #for x in range(10, 20):
        #    Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(self.map_data)
            for col, tile in enumerate(tiles):
                #Uses a string to denote an instance of a game object
                if tile == '1':
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "S":
                    Spike(self, col, row)
                    
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
         self.all_sprites.update()

    #Draw lines to make grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
             pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
             pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))
    
    #Draw grid and fill in BG
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen) 
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
    
    def show_start_screen(self):
         pass
    
    def show_go_screen(self):
         pass
         

#Instantiation of the Game class    
g = Game()
# g.show_start_screen()

while True:
     g.new()
     g.run()
     #g.show_go_screen()

#Run game
g.run()

        
