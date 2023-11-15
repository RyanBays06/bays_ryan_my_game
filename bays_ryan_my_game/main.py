#GOALS
    # Jump to new platform
    # Don't fall off map
    # Avoid mobs
#FEATURE GOALS
    # give mobs an identity
    # make platforms advance with player
    # make screen move up as player moves up
#RULES
    # Use W,A,S,D to move and space bar to jump
    # Respawn when health is below 1hp
    # Avoid mobs

# content from kids can code: http://kidscancode.org/blog/ & https://www.w3schools.com/python/python_reference.asp
# group collaboration on some small parts of code

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self): 
        # create a group for all sprites
        self.bgimage = pg.image.load(os.path.join(img_folder, 'backgroundimage1.png')).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
       

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        for m in range(0,5):
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
       
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0
        
        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if hits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("oof")
                self.player.hitpoints -= 5
                if self.player.hitpoints < 1:
                    self.player = pg.QUIT
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
        # the screen moves up when player advances to new platforms
        if self.player.rect.top <= HEIGHT / 3:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.all_platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10     
        # when player falls off the screen he will respawn            
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.all_platforms) == 0:
            self.playing = False
                    
        



    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bgimage,(0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Hitpoints: " + str(self.player.hitpoints), 22, WHITE, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
        

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

        
       
        
    
 
           

g = Game()
while g.running:
    g.new()



pg.quit()


