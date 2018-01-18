# Hit-a-Plane
bullet.py 子弹  <br />
enmey.py 敌人  <br />
myplane.py 飞机<br />
supply.py 补及<br />

part1思路：<br />
写main()<br />
1.先导入需要用到的pygame、sys、traceback模块<br />
 from pygame.locals import * 这个是导入常用函数与常量。<br />
2.初始化pygame，pygame.mixer
3.设置分辨率与背景图
4.导入音效资源
 pygame.mixer.music.load（）
 bomb_sound = pygame.mixer.Sound（）
5.写main（），播放音乐，用for循环获取时间与绘制背景图
6、if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()

part2：
优化：
1.结束游戏是隐藏暂停按钮
定义一个BUTTON_ON = True
BUTTON_ON为True是绘制按钮
结束游戏时把BUTTON_ON = False
