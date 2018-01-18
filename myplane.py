#这个设置我的飞机
import pygame

class MyPlane(pygame.sprite.Sprite):
	def __init__(self,bg_size):
		pygame.sprite.Sprite.__init__(self)

		self.image1 = pygame.image.load("images\\me1.png").convert_alpha()
		self.image2 = pygame.image.load("images\\me2.png").convert_alpha()
		self.destroy_images = [] #列表存放飞机销毁图片
		#列表末尾一次性追加另一个序列中的多个值
		self.destroy_images.extend([\
			pygame.image.load("images\\me_destroy_1.png").convert_alpha(),\
			pygame.image.load("images\\me_destroy_2.png").convert_alpha(),\
			pygame.image.load("images\\me_destroy_3.png").convert_alpha(),\
			pygame.image.load("images\\me_destroy_4.png").convert_alpha()\
			])
		self.rect = self.image1.get_rect()
		self.width,self.height = bg_size[0],bg_size[1]
		#设置飞机的出现位置
		self.rect.left,self.rect.top = \
						(self.width - self.rect.width) /2,\
						self.height - self.rect.height - 60   #底部状态栏预留60像素
		self.speed = 10
		self.active = True
		self.invincible = False #无敌状态 用于飞机重生保护
		self.mask = pygame.mask.from_surface(self.image1) #获取图标不透明部分用作碰撞检测

	def reset(self):
		self.rect.left,self.rect.top = \
						(self.width - self.rect.width) /2,\
						self.height - self.rect.height - 60
		self.active = True
		self.invincible = True
		
	#定义4个方法控制飞机移动
	def moveUp(self):
		if self.rect.top > 0:
			self.rect.top -= self.speed  #往上走减速度
		else:
			self.rect.top = 0

	def moveDown(self):
		if self.rect.bottom < self.height - 60:
			self.rect.top += self.speed   #往下走加速度
		else:
			self.rect.bottom = self.height - 60

	def moveLeft(self):
		if self.rect.left > 0:
			self.rect.left -= self.speed
		else:
			self.rect.left = 0

	def moveRight(self):
		if self.rect.right < self.width:
			self.rect.right += self.speed
		else:
			self.rect.right = self.width
