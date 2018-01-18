import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
	def __init__(self,bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("images\\enemy1.png").convert_alpha()
		self.destroy_images = []	 #列表存放飞机销毁图片
		#列表末尾一次性追加另一个序列中的多个值
		self.destroy_images.extend([\
			pygame.image.load("images\\enemy1_down1.png").convert_alpha(),\
			pygame.image.load("images\\enemy1_down2.png").convert_alpha(),\
			pygame.image.load("images\\enemy1_down3.png").convert_alpha(),\
			pygame.image.load("images\\enemy1_down4.png").convert_alpha()\
			])
		self.rect = self.image.get_rect()
		self.width,self.height = bg_size[0],bg_size[1]
		self.speed = 2
		self.active = True
		self.mask = pygame.mask.from_surface(self.image) #获取图标不透明部分用作碰撞检测
		self.rect.left,self.rect.top = \
						randint(0,self.width - self.rect.width),\
						randint(-5 * self.height,0)    #随机x y坐标，y坐标 5*height

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.reset()

	def reset(self):
		self.active = True
		self.rect.left,self.rect.top = \
						randint(0,self.width - self.rect.width),\
						randint(-5 * self.height,0)

class MidEnemy(pygame.sprite.Sprite):
	energy = 8
	def __init__(self,bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("images\\enemy2.png").convert_alpha()
		self.image_hit = pygame.image.load("images\\enemy2_hit.png").convert_alpha()
		self.destroy_images = []
		self.destroy_images.extend([\
			pygame.image.load("images\\enemy2_down1.png").convert_alpha(),\
			pygame.image.load("images\\enemy2_down2.png").convert_alpha(),\
			pygame.image.load("images\\enemy2_down3.png").convert_alpha(),\
			pygame.image.load("images\\enemy2_down4.png").convert_alpha()\
			])
		self.rect = self.image.get_rect()
		self.width,self.height = bg_size[0],bg_size[1]
		self.speed = 1
		self.active = True
		self.mask = pygame.mask.from_surface(self.image) #获取图标不透明部分用作碰撞检测
		self.energy = MidEnemy.energy
		self.hit = False  #击中状态 默认False
		self.rect.left,self.rect.top = \
						randint(0,self.width - self.rect.width),\
						randint(-10 * self.height,0)   #随机x y坐标，y坐标 10*height

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.reset()

	def reset(self):
		self.active = True
		self.energy = MidEnemy.energy
		self.rect.left,self.rect.top = \
						randint(0,self.width - self.rect.width),\
						randint(-10 * self.height,0)

class BigEnemy(pygame.sprite.Sprite):
	energy = 20
	def __init__(self,bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.image1 = pygame.image.load("images\\enemy3_n1.png").convert_alpha()
		self.image2 = pygame.image.load("images\\enemy3_n2.png").convert_alpha()
		self.image_hit = pygame.image.load("images\\enemy3_hit.png").convert_alpha()
		self.destroy_images = []
		self.destroy_images.extend([\
			pygame.image.load("images\\enemy3_down1.png").convert_alpha(),\
			pygame.image.load("images\\enemy3_down2.png").convert_alpha(),\
			pygame.image.load("images\\enemy3_down3.png").convert_alpha(),\
			pygame.image.load("images\\enemy3_down4.png").convert_alpha(),\
			pygame.image.load("images\\enemy3_down5.png").convert_alpha(),\
			pygame.image.load("images\\enemy3_down6.png").convert_alpha()\
			])
		self.rect = self.image1.get_rect()
		self.width,self.height = bg_size[0],bg_size[1]
		self.speed = 1
		self.active = True
		self.mask = pygame.mask.from_surface(self.image1) #获取图标不透明部分用作碰撞检测
		self.energy = BigEnemy.energy
		self.hit = False  #击中状态 默认False
		self.rect.left,self.rect.top = \
						randint(0,self.width - self.rect.width),\
						randint(-15 * self.height,0)      #随机x y坐标，y坐标 15*height

	def move(self):
		if self.rect.top < self.height:
			self.rect.top += self.speed
		else:
			self.reset()

	def reset(self):
		self.active = True
		self.energy = BigEnemy.energy
		self.rect.left,self.rect.top = \
						randint(0,self.width - self.rect.width),\
						randint(-15 * self.height,0)   