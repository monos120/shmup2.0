import pygame as pg
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "game jam"
BGCOLOR = BLUE
FONT = 'arial'

TILESIZE = 64
TILE_IMG = 'water.png'
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_SPEED = 350
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'player_ship.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 80, 80)
PLAYER_HEALTH = 100

CANNON_IMG = 'cannon_ball.png'
CANNON_SPEED = 1000
CANNON_LIFE = 1000
CANNON_RATE = 200
CANNON_DAMAGE = 20

MOB_IMG = 'enemy_1.png'
MOB_SPEED = random.randrange(100, 200)
MOB_HIT_RECT = pg.Rect(0, 0, 80, 80)
MOB_SPAWN_TIME = 2000
MOB_HEALTH = 100
MOB_KNOCKBACK = 20
MOB_DAMAGE = 20
MOB_SPEEDS = [150, 100, 75, 125]
AVR = 70
DTR = 50

#oh my god why was adding audio so hard
BGM = 'bgm.ogg'
OH_NO = ['oof.wav', 'ouchie.wav']
NERD_DOWN = ['yippekeeyahheeyapeeahkayoh.wav']
PEW_PEW = ['bang.wav', 'blammo.wav', 'kablooie.wav', 'bonk.wav']
WHY = 'level_start.wav'
