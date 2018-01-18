#导入模块
import pygame
import sys
import myplane
import enemy
import bullet
import supply
import traceback
from pygame.locals import *
from random import *

#初始化
pygame.init()
pygame.mixer.init()

bg_size = width,height = 480,700 #设置界面分辨率
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")			#设置标题
background = pygame.image.load("images\\background.png").convert() #设置背景图
#定义颜色
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

#导入音效资源------------
pygame.mixer.music.load("sound\\game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound\\bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound\\use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound\\supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound\\get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound\\get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound\\upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound\\enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.3)
enemy1_down_sound = pygame.mixer.Sound("sound\\enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound\\enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound\\enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound\\me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1,group2,num):
	for i in range(num):
		e1 = enemy.SmallEnemy(bg_size) #实例化敌机
		group1.add(e1)   #添加进组
		group2.add(e1)

def add_mid_enemies(group1,group2,num):
	for i in range(num):
		e1 = enemy.MidEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def add_big_enemies(group1,group2,num):
	for i in range(num):
		e1 = enemy.BigEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def inc_speed(target,inc):
	for each in target:
		each.speed += inc

def main():

	pygame.mixer.music.play(-1)	#播放背景音乐
	me = myplane.MyPlane(bg_size)	#生成我方飞机
	enemies = pygame.sprite.Group() #敌方机组
	#生成小型敌机
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies,enemies,15)
	#生成中型敌机
	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies,enemies,4)
	#生成大型敌机
	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies,enemies,2)
	#生成普通子弹
	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4
	for i in range(BULLET1_NUM):
		bullet1.append(bullet.Bullet1(me.rect.midtop)) #实例化子弹，生成在图片顶部中间

	#生成超级子弹
	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 8
	for i in range(BULLET2_NUM//2):
		bullet2.append(bullet.Bullet2((me.rect.centerx-33,me.rect.centery)))#实例化子弹，生成在图片顶部中间
		bullet2.append(bullet.Bullet2((me.rect.centerx+30,me.rect.centery)))

	clock = pygame.time.Clock()
	running = True #用于主循环
	switch_image = True #用于切换图片
	delay = 100 #用于延迟
	#中弹索引
	e1_destroy_index = 0
	e2_destroy_index = 0
	e3_destroy_index = 0
	me_destroy_index = 0
	#统计分数
	score = 0
	score_font = pygame.font.Font("font/font.ttf",36) #定义字体
	#标记是否暂停游戏
	paused = False
	paused_nor_image = pygame.image.load("images\\pause_nor.png").convert_alpha()
	paused_pressed_image = pygame.image.load("images\\pause_pressed.png").convert_alpha()
	resume_nor_image = pygame.image.load("images\\resume_nor.png").convert_alpha()
	resume_pressed_image = pygame.image.load("images\\resume_pressed.png").convert_alpha()
	paused_rect = paused_nor_image.get_rect()
	paused_rect.left,paused_rect.top = width - paused_rect.width - 10 ,10  #设置暂停按钮位置
	paused_image = paused_nor_image

	#游戏结束画面
	gameover_font = pygame.font.Font("font\\font.ttf",48)
	again_image = pygame.image.load("images\\again.png").convert_alpha()
	again_rect = again_image.get_rect()
	gameover_image = pygame.image.load("images\\gameover.png").convert_alpha()
	gameover_rect = gameover_image.get_rect()


	#设置游戏级别
	level = 1

	#炸弹
	bomb_image = pygame.image.load("images\\bomb.png").convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font("font\\font.ttf",48)
	bomb_num = 3

	#每30秒发放一个补给包，实例化子弹与炸弹
	bullet_supply = supply.Bullet_Supply(bg_size)
	bomb_supply = supply.Bomb_Supply(bg_size)
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME,30 * 1000)

	#超级子弹定时器
	DOUBLE_BULLET_TIME = USEREVENT + 1

	#标记是否使用超级子弹
	is_double_bullet = False

	#解除我方飞机重生保护状态
	INVINCIBLE_TIME = USEREVENT + 2

	#我方飞机生命数量
	life_image = pygame.image.load("images\\life.png").convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3

	#用于阻止重复打开记录文件record.txt
	recorded = False



	#--------循环主体---------------
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			#判断暂停按钮与继续按钮进行切换
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused
					#暂停时音效暂停播放
					if paused:
						pygame.time.set_timer(SUPPLY_TIME,0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					else:
						pygame.time.set_timer(SUPPLY_TIME,3 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()

			elif event.type == MOUSEMOTION:
				if paused_rect.collidepoint(event.pos):
					if paused:
						paused_image = resume_pressed_image
					else:
						paused_image = paused_pressed_image
				else:
					if paused:
						paused_image = resume_nor_image
					else:
						paused_image = paused_nor_image

			#按下空格释放炸弹，数量递减 播放音效 销毁飞机
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if bomb_num:
						bomb_num -= 1
						bomb_sound.play()
						for each in enemies:
							if each.rect.bottom > 0:
								each.active = False

			elif event.type == SUPPLY_TIME:
				supply_sound.play()
				if choice([True,False]):
					bomb_supply.reset()
				else:
					bullet_supply.reset()

			elif event.type ==DOUBLE_BULLET_TIME:
				is_double_bullet = False
				pygame.time.set_timer(DOUBLE_BULLET_TIME,0) #关闭定时器

			elif event.type == INVINCIBLE_TIME:
				me.invincible = False
				pygame.time.set_timer(INVINCIBLE_TIME,0)


		#根据得分更改游戏等级
		if level == 1 and score > 5000:
			level = 2
			upgrade_sound.play()
			#增加3架小型敌机，2架中型敌机和1架大型敌机
			add_small_enemies(small_enemies,enemies,3)
			add_mid_enemies(mid_enemies,enemies,2)
			add_big_enemies(big_enemies,enemies,1)
			#提升小型敌机速度
			inc_speed(small_enemies,1)
		elif level == 2 and score > 300000:
			level = 3
			upgrade_sound.play()
			#增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升敌机速度
			inc_speed(small_enemies,1)
			inc_speed(mid_enemies,1)
		elif level == 3 and score > 600000:
			level = 4
			upgrade_sound.play()
			#增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升敌机速度
			inc_speed(small_enemies,1)
			inc_speed(mid_enemies,1)
		elif level == 4 and score > 1000000:
			level = 5
			upgrade_sound.play()
			#增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升敌机速度
			inc_speed(small_enemies,1)
			inc_speed(mid_enemies,1)
		elif level == 5 and score > 5000000:
			level = 5
			upgrade_sound.play()
			#增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升敌机速度
			inc_speed(small_enemies,1)
			inc_speed(mid_enemies,1)

		screen.blit(background,(0,0))	#绘制背景,把绘制背景放到前面，在暂停是遮挡换面，防作弊

		#有剩余生命（life_num不为零） 和 没有暂停执行子循环
		if life_num and not paused:
			#检查用户键盘操作
			key_pressed = pygame.key.get_pressed()

			if key_pressed[K_w] or key_pressed[K_UP]:
				me.moveUp()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.moveDown()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.moveLeft()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.moveRight()

			#绘制全屏炸弹补给并检查是否获得
			if bomb_supply.active:
				bomb_supply.move()
				screen.blit(bomb_supply.image,bomb_supply.rect)
				if pygame.sprite.collide_mask(bomb_supply,me):
					get_bomb_sound.play()
					if bomb_num < 3:
						bomb_num += 1
					bomb_supply.active = False

			#绘制超级子弹补给并检查是否获得
			if bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image,bullet_supply.rect)
				if pygame.sprite.collide_mask(bullet_supply,me):
					get_bullet_sound.play()
					#发射超级子弹
					is_double_bullet = True
					pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
					bullet_supply.active = False

	        #-----------------图片绘制--------------------	
			
			#每当被10整除 调用一次，相当于没10帧发射一颗子弹
			if not(delay % 10): 
				bullet_sound.play()
				if is_double_bullet:
					bullets = bullet2
					bullets[bullet2_index].reset((me.rect.centerx - 33,me.rect.centery))
					bullets[bullet2_index+1].reset((me.rect.centerx + 30,me.rect.centery))
					bullet2_index = (bullet2_index + 2) % BULLET2_NUM
				else:
					bullets = bullet1
					bullets[bullet1_index].reset(me.rect.midtop)  #设置子弹位置在飞机顶端中央
					bullet1_index = (bullet1_index + 1) % BULLET1_NUM #

			#检查子弹是否击中飞机
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image,b.rect)
					enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
					if enemy_hit:
						b.active = False
						for e in enemy_hit:
							if e in mid_enemies or e in big_enemies:
								e.hit = True   #被击中时为True
								e.energy -= 1
								if e.energy == 0:
									e.active = False
							else:
								e.active = False



			#绘制大型飞机
			for each in big_enemies:
				if each.active:
					each.move()
					if each.hit:
						screen.blit(each.image_hit,each.rect)
						each.hit = False
					else:
						if switch_image:
							screen.blit(each.image1,each.rect)
						else:
							screen.blit(each.image2,each.rect)
					#绘制血槽
					pygame.draw.line(screen,BLACK,\
						(each.rect.left,each.rect.top - 5),\
						(each.rect.left,each.rect.top - 5),2)
					#当生命对于20%显示绿色，否则显示红色
					energy_remain = each.energy / enemy.BigEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen,energy_color,\
						(each.rect.left,each.rect.top - 5),\
						(each.rect.left + each.rect.width * energy_remain,\
						each.rect.top - 5),2)

						#即将出现画面时，播放音效
					if each.rect.bottom == -50:
						enemy3_fly_sound.play(-1) #-1循环播放
				else:
					if e3_destroy_index == 0:
						#播放销毁图片及音效
						enemy3_down_sound.play()
					#active = False 时毁灭飞机；
					#delay % 3 是 取模余3是进延迟播放
					if not(delay % 3):
						screen.blit(each.destroy_images[e3_destroy_index],each.rect)
						e3_destroy_index =(e3_destroy_index + 1) % 6
						if e3_destroy_index == 0:
							enemy3_fly_sound.stop()
							score += 10000 #在敌机销毁时加分数
							each.reset()  #重置位置

			


			#绘制中型飞机
			for each in mid_enemies:
				if each.active:
					each.move()
					if each.hit:
						screen.blit(each.image_hit,each.rect)
						each.hit = False
					else:
						screen.blit(each.image,each.rect)

					#绘制血槽
					pygame.draw.line(screen,BLACK,\
						(each.rect.left,each.rect.top - 5),\
						(each.rect.left,each.rect.top - 5),2)
					#当生命对于20%显示绿色，否则显示红色
					energy_remain = each.energy / enemy.MidEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen,energy_color,\
						(each.rect.left,each.rect.top - 5),\
						(each.rect.left + each.rect.width * energy_remain,\
						each.rect.top - 5),2)
				else:
					if e2_destroy_index == 0:
						#active = False 时毁灭飞机；播放销毁图片及音效
						enemy2_down_sound.play()
					#delay % 3 是 取模余3是进延迟播放
					if not(delay % 3):
						screen.blit(each.destroy_images[e2_destroy_index],each.rect)
						e2_destroy_index =(e2_destroy_index + 1) % 4
						if e2_destroy_index == 0:
							score += 6000 #在敌机销毁时加分数
							each.reset()  #重置位置


			#绘制小型飞机
			for each in small_enemies:
				if each.active:
					each.move()
					screen.blit(each.image,each.rect)
				else:
					if e1_destroy_index == 0:
						#active = False 时毁灭飞机；播放销毁图片及音效
						enemy1_down_sound.play()
					#delay % 3 是 取模余3是进延迟播放
					if not(delay % 3):
						screen.blit(each.destroy_images[e1_destroy_index],each.rect)
						e1_destroy_index =(e1_destroy_index + 1) % 4
						if e1_destroy_index == 0:
							score += 1000 #在敌机销毁时加分数
							each.reset()  #重置位置				

			#检测我方飞机是否被撞
			enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
			if enemies_down and not me.invincible:
				me.active = False
				for  e in enemies_down:
					e.active = False


			#绘制我方飞机	
			if me.active:	
				if switch_image:
					screen.blit(me.image1,me.rect)	
				else:
					screen.blit(me.image2,me.rect)
			else:
				#active = False 时毁灭飞机；播放销毁图片及音效
				me_down_sound.play()
				#delay % 3 是 取模余3是进延迟播放
				if not(delay % 3):
					screen.blit(me.destroy_images[me_destroy_index],me.rect)
					me_destroy_index =(me_destroy_index + 1) % 4
					if me_destroy_index == 0:
						life_num-= 1
						me.reset()  #重置位置
						pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

			#绘制炸弹数量
			bomb_text = bomb_font.render("x %d"% bomb_num,True,WHITE)
			text_rect = bomb_image.get_rect()
			screen.blit(bomb_image,(10,height - 10 - bomb_rect.height))
			screen.blit(bomb_text,(20 + bomb_rect.width,height - 5 - text_rect.height))

			#绘制飞机生命剩余数量
			if life_num:
				for  i in range(life_num):
					screen.blit(life_image,(width -10-(i+1)*life_rect.width,\
								height - 10 -life_rect.height))
			#绘制分数界面
			score_text = score_font.render("Score: %s " %str(score),True,WHITE)	
			screen.blit(score_text,(10,5))	

		
		#绘制游戏结束画面
		elif life_num == 0:
			#停止背景音乐
			pygame.mixer.music.stop()
			#停止音效
			pygame.mixer.stop()
			#停止发放补给
			pygame.time.set_timer(SUPPLY_TIME,0)

			if not recorded:
				recorded = True
				#读取历史最高得分
				with open("record.txt","r") as f:
					record_score = int(f.read())
				if score > record_score:
					with open("record.txt","w") as f:
						f.write(str(score))

			#绘制结束画面
			record_score_text = score_font.render("Best:%s"%record_score,True,WHITE)
			screen.blit(record_score_text,(50,50))	

			gameover_text1 = gameover_font.render("Your Score",True,WHITE)
			gameover_text1_rect = gameover_text1.get_rect()
			gameover_text1_rect.left,gameover_text1_rect.top = (width - gameover_text1_rect.width) //2, height//3
			screen.blit(gameover_text1,gameover_text1_rect)

			gameover_text2 = gameover_font.render(str(score),True,WHITE)
			gameover_text2_rect = gameover_text2.get_rect()
			gameover_text2_rect.left,gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2,\
															gameover_text1_rect.bottom + 10
			screen.blit(gameover_text2,gameover_text2_rect)

			again_rect.left,again_rect.top = (width - again_rect.width) // 2,\
											gameover_text2_rect.bottom + 50
			screen.blit(again_image,again_rect)

			gameover_rect.left,gameover_rect.top = (width - gameover_rect.width) // 2,\
											again_rect.bottom + 10
			screen.blit(gameover_image,gameover_rect)

			#检测用户的鼠标操作
			#如果用户按下鼠标左键
			if pygame.mouse.get_pressed()[0]:
				#获取鼠标坐标
				pos = pygame.mouse.get_pos()
				#如果用户点击“重新开始”
				if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] <again_rect.bottom:
					main()
				#如果用户点击“结束游戏”
				elif gameover_rect.left < pos[0] < gameover_rect.right and \
						gameover_rect.top < pos[1] < gameover_rect.bottom:
					pygame.quit()
					sys.exit()

		#绘制暂停按钮
		screen.blit(paused_image,paused_rect)


		if not(delay % 5):
			switch_image = not switch_image  #在循环里不断切换状态
		#延时器
		delay -= 1
		if not delay:
			delay = 100
		
		pygame.display.flip()		#刷新画面
		clock.tick(60)				#每秒60帧



if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()