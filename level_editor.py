import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#oyun  ekranı
#başlık boyutu
tile_size = 30
#sütunlar
cols = 20
#kenar
margin = 100
#genişlik
screen_width =600
#yükseklik
screen_height = 750
	
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#GÖRSELLER
sun_img = pygame.image.load('img/sun.png')
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
bg_img2 = pygame.image.load('img/sky5.png')  # New background image
bg_img2 = pygame.transform.scale(bg_img2, (screen_width, screen_height - margin))  # Adjust size if needed
bg_img3 = pygame.image.load('img/sky3.png')  # New background image
bg_img3 = pygame.transform.scale(bg_img3, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('img/dirt.png')
stone_img=pygame.image.load('img/stone.png')
brick_img=pygame.image.load('img/brick.png')
grass_img = pygame.image.load('img/grass.png')
grass_img2=pygame.image.load('img/grass2.png')
grass_img3=pygame.image.load('img/grass3.png')
blob_img = pygame.image.load('img/blob.png')
blob2_img=pygame.image.load('img/blob2.png')
platform_x_img = pygame.image.load('img/platform_x.png')
platform_x2_img=pygame.image.load('img/platform_x2.png')
platform_y_img = pygame.image.load('img/platform_y.png')
platform_y2_img=pygame.image.load('img/platform_y2.png')
lava_img = pygame.image.load('img/lava.png')
lava_img2=pygame.image.load('img/lava2.png')
coin_img = pygame.image.load('img/cheese.png')
coin_img2=pygame.image.load('img/cheese2.png')
exit_img = pygame.image.load('img/exit.png')
exit_img2=pygame.image.load('img/exit2.png')
save_img = pygame.image.load('img/save_btn.png')
load_img = pygame.image.load('img/load_btn.png')


#OYUN DEĞİŞKENLERİ
clicked = False
level = 1

#RENKLER
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#boş dünya yaratma
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

#sınırlar
for tile in range(0, 20):
	world_data[19][tile] = 2
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1

#metinleri ekrana yazdırma kodları
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(21):
		#dikey çizgi
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
		#yatay çizgi
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
	for row in range(20):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#TOPRAK
					if level > 5 and level<=10:  
						img = pygame.transform.scale(stone_img, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
					elif level>10 and level<=15:
						img = pygame.transform.scale(brick_img, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
					else :
						img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#ÇİMLİ TOPRAK
					if level>5 and level<=10:
						img = pygame.transform.scale(grass_img2, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
					elif level>10 and level<=15:
						img = pygame.transform.scale(grass_img3, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
					else:
						img = pygame.transform.scale(grass_img, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#DÜŞMAN 
					if level>5 and level<=10:
						img=pygame.transform.scale(blob2_img,(tile_size,tile_size))
						screen.blit(img,(col*tile_size,row * tile_size))
					else:
						img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
						screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					#YATAY HAREKETLİ BLOK
					if level> 5:
						img = pygame.transform.scale(platform_x2_img, (tile_size, tile_size // 2))
						screen.blit(img, (col * tile_size, row * tile_size))
					else:
						img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
						screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#DİKEY HAREKETLİ BLOK
					if level>5:
						img = pygame.transform.scale(platform_y2_img, (tile_size, tile_size // 2))
						screen.blit(img, (col * tile_size, row * tile_size))
					else:	
						img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
						screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					#DİKENLER
					if level>5:
						img=pygame.transform.scale(lava_img2, (tile_size, tile_size // 2))
						screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
					else:	
						img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
						screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					#ÖDÜL
					if level >5:
						img = pygame.transform.scale(coin_img2, (tile_size // 2, tile_size // 2))
						screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
					else:
						img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
						screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					#ÇIKIŞ
					if level > 5:  
						img = pygame.transform.scale(exit_img2, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))
					else :
						img = pygame.transform.scale(exit_img, (tile_size, tile_size))
						screen.blit(img, (col * tile_size, row * tile_size))



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#Mouse konumunu
		pos = pygame.mouse.get_pos()

		#Mouse ile üzerine gelme ve tıklama
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#Kaydetme ve yükleme butonu kodları
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

#Oyun Loopu
run = True
while run:

	clock.tick(fps)

	#seviyeler değiştikçe görsellerin değişmesi
	screen.fill(green)
	
	if level > 5 and level<=10:  
				# 6-7-8-9-10 seviye görselleri
				screen.blit(bg_img2, (0, 0))  
	elif level>10 and level<16:
				#11-12-13-14-15 seviye görseli
				screen.blit(bg_img3, (0, 0)) 
	else:
				# 1-2-3-4-5 seviye görselleri
				screen.blit(bg_img, (0, 0))  

	#seviye kaydetme ve seviyeyi yükleme kodları
	save_clicked = save_button.draw()
	if save_clicked:
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
		# Kaydetme işlemi başarılı mesajı
		draw_text('BASARIYLA KAYDEDİLDİ', font, white, tile_size, screen_height - 80)

	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#Izgara ve seviyeyi çizdirmeyi gösteren kodlar
	draw_grid()
	draw_world()


	# Gösterilen seviyeyi gösteren metinler
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

	# etkinlikler
	for event in pygame.event.get():
		# Oyundan çıkış
		if event.type == pygame.QUIT:
			run = False
		# Eklemeleri değiştirmek için mouse tıklamaları
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			# Kordinatların ekleme alanı içerisinde olmasının kontrol eden kodlar
			if x < 20 and y < 20:
				# Ekleme değerleri 
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 8:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 8
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		# Seviyelerin değişmesi için yukarı veya aşağı basılma tuşları kodları
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1
			elif event.key == pygame.K_y:
				# 'y' tuşuna basıldığında kaydetme işlemi
				pickle_out = open(f'level{level}_data', 'wb')
				pickle.dump(world_data, pickle_out)
				pickle_out.close()


	#Oyun ekranını güncelleme
	pygame.display.update()

pygame.quit()