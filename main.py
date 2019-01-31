import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from camera_and_stuff import *

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        pg.mixer.music.play(loops = -1)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        aud_folder = path.join(game_folder, 'aud')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (TILESIZE, TILESIZE))
        self.cannon_img = pg.image.load(path.join(img_folder, CANNON_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (TILESIZE, TILESIZE))
        self.tile_img = pg.image.load(path.join(img_folder, TILE_IMG)).convert_alpha()
        #music stuff
        pg.mixer.music.load(path.join(aud_folder, BGM))
        self.level_start = pg.mixer.Sound(path.join(aud_folder, WHY))
        self.shoot_sounds = {}
        self.shoot_sounds['cannon'] = []
        for snd in PEW_PEW:
            self.shoot_sounds['cannon'].append(pg.mixer.Sound(path.join(aud_folder, snd)))
        self.ouch = []
        for snd in OH_NO:
            self.ouch.append(pg.mixer.Sound(path.join(aud_folder, snd)))
        self.nerd_down = []
        for snd in NERD_DOWN:
            self.nerd_down.append(pg.mixer.Sound(path.join(aud_folder, snd)))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.cannons = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    self.image = self.tile_img
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.level_start.play()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            choice(self.ouch).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.death_screen()
                self.new()
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        hits = pg.sprite.groupcollide(self.mobs, self.cannons, False, True)
        for hit in hits:
            hit.health -= CANNON_DAMAGE
            hit.vel = vec(0, 0)
        if len(self.mobs) == 0:
            self.show_game_over()
            self.new()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(path.join('redline.ttf'), 40)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        pg.display.set_caption("SEA INVADER")
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Enemies: {}'.format(len(self.mobs)), 30, WHITE, WIDTH - 120, 10)
        pg.display.flip()
		
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
					
    def uhhh(self):
         waiting = True
         while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("SEA INVADER", 48, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text("WASD to move, space to shoot.", 28, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.wait_for_key()
		
    def death_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("INVADERS WIN!", 64, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press space to play again.", 24, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.uhhh()
			
    def show_game_over(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("YOU WIN!", 64, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press space to play again.", 24, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.uhhh()
	
g = Game()
while True:
    g.show_start_screen()
    g.new()
    g.run()
