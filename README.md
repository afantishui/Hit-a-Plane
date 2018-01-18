# Hit-a-Plane
bullet.py 子弹  <br />
enmey.py 敌人  <br />
myplane.py 飞机<br />
supply.py 补及<br />

part1思路：<br />
写main()<br />
1.先导入需要用到的pygame、sys、traceback模块<br />
 from pygame.locals import * 这个是导入常用函数与常量。<br />
2.初始化pygame，pygame.mixer<br />
3.设置分辨率与背景图<br />
4.导入音效资源<br />
 pygame.mixer.music.load（）<br />
 bomb_sound = pygame.mixer.Sound（）<br />
5.写main（），播放音乐，用for循环获取时间与绘制背景图<br />
6、if __name__ == '__main__':<br />
	try:<br />
		main()<br />
	except SystemExit:<br />
		pass<br />
	except:<br />
		traceback.print_exc()<br />
		pygame.quit()<br />
		input()<br />

part2：<br />
优化：<br />
1.结束游戏是隐藏暂停按钮<br />
定义一个BUTTON_ON = True<br />
BUTTON_ON为True是绘制按钮<br />
结束游戏时把BUTTON_ON = False<br />

效果图：<br />
![Image text](https://github.com/afantishui/Hit-a-Plane/blob/master/playing.png)<br />
![Image text](https://github.com/afantishui/Hit-a-Plane/blob/master/gameover.png)<br />
