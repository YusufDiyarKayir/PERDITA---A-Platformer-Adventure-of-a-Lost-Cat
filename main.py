import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()




clock = pygame.time.Clock()
fps = 60

tile_size = 50
cols = 20
margin = 100
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('PERDITA')


#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)


#define game variabes
tile_size = 50
game_over = 0
main_menu = True
level = 11
max_levels = 15
score = 0
death = 0

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)


#load images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
continue_img=pygame.image.load('img/pause.png')
sound_img=pygame.image.load('img/pause.png')
menu_img=pygame.image.load('img/menu.png')
next_img=pygame.image.load('img/next.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
bg_img2 = pygame.image.load('img/sky5.png')
bg_img2 = pygame.transform.scale(bg_img2, (screen_width, screen_height))
bg_img3 = pygame.image.load('img/sky3.png')
bg_img3 = pygame.transform.scale(bg_img3, (screen_width, screen_height))
sun_img = pygame.transform.scale(sun_img, (100, 100))
#load sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 1000)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(1.5)
show_story = True
story_index = 0
show_story2 = False
story_index2 = 0
show_story_finish = False
story_index_finish = 0
sound_on = True


# load story images
story_images = [
	pygame.image.load('img/sprite_0.png'),
    pygame.image.load('img/story_0.png'),
    pygame.image.load('img/story_1.png'),
    pygame.image.load('img/story_2.png'),
    pygame.image.load('img/story_4.png'),
    pygame.image.load('img/story_5.png')
]
story_images = [pygame.transform.scale(img, (screen_width, screen_height)) for img in story_images]

story_images2 = [
	pygame.image.load('img/Story2.1.png'),
    pygame.image.load('img/Story2.2.png'),
	pygame.image.load('img/Story2.3.png'),
	pygame.image.load('img/Story2.4.png'),
	pygame.image.load('img/Story2.5.png'),
    
]
story_images2 = [pygame.transform.scale(img, (screen_width, screen_height)) for img in story_images2]

story_images_finish = [
	pygame.image.load('img/sprite_0.png'),
    pygame.image.load('img/story_0.png'),
    pygame.image.load('img/story_1.png'),
    pygame.image.load('img/story_2.png'),
    pygame.image.load('img/story_4.png'),
    pygame.image.load('img/story_5.png')
]
story_images_finish = [pygame.transform.scale(img, (screen_width, screen_height)) for img in story_images_finish]

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function to reset level
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
        world = World(world_data)
    else:
        world_data = []  #
        world = World(world_data)
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)

    return world



class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

    def reset(self):
        self.clicked = False



class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			
			self.in_air = True
			for tile in world.tile_list:
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		img_right = pygame.image.load(f'img/cat_walk.png')
		img_right = pygame.transform.scale(img_right, (40, 80))
		img_left = pygame.transform.flip(img_right, True, False)
		self.images_right.append(img_right)
		self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True



class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		stone_img = pygame.image.load('img/stone.png')
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')
		brick_img=pygame.image.load('img/brick.png')
		grass_img3 = pygame.image.load('img/grass3.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(stone_img if level > 5 and level<11 else brick_img if level>10 else dirt_img, (tile_size, tile_size))  # Değiştirildi
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img3 if level>10 else grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])



class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		if level>5 and level<11:
			self.image=pygame.image.load('img/blob2.png')
		else:
			self.image = pygame.image.load('img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		if level> 5 and level<11:
			img = pygame.image.load('img/platform2.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		elif level>10:
			img = pygame.image.load('img/platform3.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		else:
			img = pygame.image.load('img/platform.png')
			self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.start_y = y  # Yeni eklenen satır: platformun başlangıç y konumu
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y
	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1





class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		if level>5 and level<11:
			img=pygame.image.load('img/lava2.png')
		else:
			img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/cheese.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		if level >5 and level<11:
			img=pygame.image.load('img/exit2.png')
		else:
			img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



player = Player(screen_width // 2, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)


#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
next_button=Button(screen_width //2, screen_height // 2, next_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
main_menu_button=Button(screen_width // 2+50 , screen_height // 2, menu_img)
continue_button=Button(screen_width //2 -150  , screen_height // 2, continue_img)
# Buton resimlerini yükleme (resim dosyalarınızın mevcut olduğundan emin olun)
mute_img = pygame.image.load('img/sound0.png')
unmute_img = pygame.image.load('img/soundof.png')

# Mute ve unmute butonlarını tanımlama
mute_button = Button(screen_width // 2-150, screen_height // 2+100, mute_img)
unmute_button = Button(screen_width // 2+50 , screen_height // 2 + 100, unmute_img)

# Sesin açık olup olmadığını takip eden değişken
muted = False


run = True
paused = False
# Değişkenlerin başlangıç değerleri
show_story2 = False
story_index2 = 0
while run:
    clock.tick(fps)
    
    events = pygame.event.get()  # Olayları bir kez al
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC tuşuna basıldığında
                paused = not paused  # Oyunun durumu değişir

    if not paused:
        if level > 5 and level < 11:
            screen.blit(bg_img2, (0, 0))
            screen.blit(sun_img, (0, 0))
        elif level > 10 and level < 16:
            screen.blit(bg_img3, (0, 0))
            screen.blit(sun_img, (0, 0))
        else:
            screen.blit(bg_img, (0, 0))
            screen.blit(sun_img, (100, 100))


        if main_menu:
            if exit_button.draw():
                run = False
            if start_button.draw():
                main_menu = False
				
        else:
            # Hikaye ekranını gösterme kontrolü
            if show_story:
                screen.blit(story_images[story_index], (0, 0))
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        story_index += 1
                        if story_index >= len(story_images):
                            show_story = False
            # Yeni hikaye ekranı kontrolü
            elif show_story2:
                screen.blit(story_images2[story_index2], (0, 0))
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        story_index2 += 1
                        if story_index2 >= len(story_images2):
                            show_story2 = False
                            level = 6
                            world = reset_level(level)
                            game_over = 0  # Yeni seviyeye geçerken game_over'ı sıfırla
            # Final hikaye ekranı kontrolü
            else:
                world.draw()

                if game_over == 0:
                    blob_group.update()
                    platform_group.update()
                    # Güncelleme yapılacaklar
                    if pygame.sprite.spritecollide(player, coin_group, True):
                        score += 1
                        if not muted:
                            coin_fx.play()
                    draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
                
                blob_group.draw(screen)
                platform_group.draw(screen)
                lava_group.draw(screen)
                coin_group.draw(screen)
                exit_group.draw(screen)

                game_over = player.update(game_over)

                # Oyuncu öldüğünde
                if game_over == -1:
                    if restart_button.draw():
                        world_data = []
                        world = reset_level(level)
                        game_over = 0
                        score = 0
                        restart_button.reset()

                # Oyuncu kazandığında
                if game_over == 1:
                    if level == 5:  # Level 5 bittiğinde
                        show_story2 = True  # Yeni hikaye ekranını göster
                        story_index2 = 0  # Yeni hikaye dizisinin başlangıç indexi
                    elif level == 10:  # Level 10 bittiğinde
                        show_story_finish = True  # Final hikaye ekranını göster
                        story_index_finish = 0  # Final hikaye dizisinin başlangıç indexi
                    elif next_button.draw():
                        level += 1
                        if level <= max_levels:
                            world_data = []
                            world = reset_level(level)
                            game_over = 0
                        else:
                            draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
                            if restart_button.draw():
                                level = 1
                                world_data = []
                                world = reset_level(level)
                                game_over = 0
                                score = 0
    else:  # Oyun durduğunda
        if continue_button.draw():
            paused = False  # Devam et butonuna basıldığında oyun devam eder
        if main_menu_button.draw():
            main_menu = True  # Ana menüye dön butonuna basıldığında ana menüye döner
            paused = False
        if not muted:
            if mute_button.draw():
                muted = True
                pygame.mixer.music.set_volume(0)
        else:
            if unmute_button.draw():
                muted = False
                pygame.mixer.music.set_volume(1)
            
    pygame.display.update()

pygame.quit()	