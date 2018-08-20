# -*- coding: utf-8 -*-

import pygame
from pygame.locals import Rect
from sys import exit
import sys

global Stage  # 关卡
global time_passed_seconds  # 刷新周期


# 角色类
class Chara(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.jumphigh = 120      # 跳跃高度
		self.Move_jump = 0       # 跳跃状态
		self.Move_left = False   # 左移判定
		self.Move_right = False  # 右移判定
		self.Move_up = False     # 上移判定
		self.Move_down = False   # 下移判定
		self.Move_fall = True    # 下落判定
		self.P_x = screen.get_width() / 2 - 48    # 角色 x 轴
		self.P_y = screen.get_height() / 2 - 96   # 角色 y 轴

		# sprite初始化设定
		self.image = None
		self.master_image = None
		self.rect = None
		self.topleft = 0, 0
		self.frame = 0
		self.old_frame = -1
		self.frame_width = 1
		self.frame_height = 1
		self.width = 1
		self.height = 1
		self.first_frame = 0
		self.last_frame = 0
		self.columns = 1
		self.last_time = 0

		self.speed = 4  # 移动速度
		self.orgin_y = self.P_y   # 跳跃初始 y 轴位置
		self.fallspeed = 0  # 下落速度
		self.jumpspeed = 0  # 跳跃速度
		self.jumpset = 0    # 跳跃状态
		self.fallset = 0    # 下落状态
		self.ground = 390 - 96  # 起跳后的地板位置
		self.jumplevel = 0  # 跳跃阶层

	def load(self, filename, width, height, columns):
		self.master_image = pygame.image.load(filename)
		self.frame_width = width
		self.frame_height = height
		self.width = width
		self.height = height
		self.rect = Rect(self.P_x, self.P_y, width, height)
		self.columns = columns
		rect = self.master_image.get_rect()
		self.last_frame = (rect.width // width) * (rect.height // height) - 1
		self.mask = pygame.mask.from_surface(self.master_image)

	def update(self, current_time, rate=200):
		if current_time > self.last_time + rate:
			self.frame += 1
			if self.frame > self.last_frame:
				self.frame = self.first_frame
			self.last_time = current_time

		if self.frame != self.old_frame:
			frame_x = (self.frame % self.columns) * self.frame_width
			frame_y = (self.frame // self.columns) * self.frame_height
			rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
			self.image = self.master_image.subsurface(rect)
			self.old_frame = self.frame
		self.rect = Rect(self.P_x, self.P_y, self.frame_width, self.frame_height)  # 位置刷新

	# 移动
	def move(self):
		distance = self.speed * time_passed_seconds
		self.fallspeed = self.jumphigh / (time_passed_seconds * 36)
		# 跳跃状态
		if (self.Move_jump == 4):
			self.orgin_y = self.P_y
			self.jumpspeed = self.jumphigh / (time_passed_seconds * 36)
			self.jumpset = 8
			self.Move_jump = 1
			self.fallset = 0
		elif (self.Move_jump == 1) and (self.orgin_y == self.P_y):
			self.P_y -= self.jumpspeed * time_passed_seconds * self.jumpset
			self.jumpset -= 1
			self.fallset = 0
		elif (self.Move_jump == 1) & (self.orgin_y > self.P_y) & (self.jumpset > 0):
			self.P_y -= self.jumpspeed * time_passed_seconds * self.jumpset
			self.jumpset -= 1
			self.fallset = 0
		elif (self.Move_jump == 1) & (self.jumpset == 0):
			self.Move_jump = 2
			self.jumpset += 1
			self.P_y += self.jumpspeed * time_passed_seconds * self.jumpset
			self.fallset = 0
		elif (self.Move_jump == 2) & (self.jumpset < 8):
			self.jumpset += 1
			self.P_y += self.jumpspeed * time_passed_seconds * self.jumpset
			self.fallset = 0
		elif (self.Move_jump == 2) & (self.jumpset == 8):
			self.P_y = self.orgin_y
			self.Move_jump = 0

		if (self.Move_jump == 0) & (self.Move_fall):
			self.P_y += self.fallspeed * time_passed_seconds * self.fallset
			self.fallset += 1

		# 左移状态
		if self.Move_left:
			if(self.P_x >= distance):
				self.P_x -= distance

		# 右移状态
		elif self.Move_right:
			if(self.P_x <= (screen.get_width() - 48 - distance)):
				self.P_x += distance

		# 上移状态
		elif self.Move_up:
			if(self.P_y >= distance):
				self.P_y -= distance

		# 下移状态
		elif self.Move_down:
			if(self.P_y <= (screen.get_height() - 96 - distance)):
				self.P_y += distance

	# 控制判定
	def control(self, stopup, stopdown, stopleft, stopright, stopjump):

		for event in pygame.event.get():
			# 游戏退出判定
			if event.type == pygame.QUIT:
				exit()

			# 游戏按键判定
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_o):   # o 键，用于调试数据输出
					print("jumplevel %d " % self.jumplevel)
					print("ground %d " % self.ground)
					print("P_y %d " % self.P_y)
				if(event.key == pygame.K_d):   # d 右移
					self.Move_right = True
				if(event.key == pygame.K_a):   # a 左移
					self.Move_left = True

				# 第二关
				if(Stage == 2):
					if(event.key == pygame.K_w) & (self.Move_jump == 0):
						self.Move_jump = 4
				# 第一关
				elif(Stage == 1):
					if(event.key == pygame.K_w):
						self.Move_up = True
					if(event.key == pygame.K_s):
						self.Move_down = True

			if(event.type == pygame.KEYUP):
				if(event.key == pygame.K_d):
					self.Move_right = False
				if(event.key == pygame.K_a):
					self.Move_left = False
				if(Stage == 1):
					if(event.key == pygame.K_w):
						self.Move_up = False
					if(event.key == pygame.K_s):
						self.Move_down = False

		# 第二关特定 跳跃阶层设定
		if (Stage == 2):
			if (self.P_y <= 84):
				self.jumplevel = 4
			elif (self.P_y <= 124):
				self.jumplevel = 3
			elif (self.P_y <= 164):
				self.jumplevel = 2
			elif (self.P_y <= 204):
				self.jumplevel = 1
			elif (self.P_y <= 294):
				self.jumplevel = 0

			if (self.jumplevel == 0):
				self.ground = 390 - 96
				if (self.P_y > 274):
					self.fallset = 0
					self.P_y = self.ground
			elif (self.jumplevel == 1):
				self.ground = 300 - 96
				if((self.P_x < 310) & (self.P_x > 142) & (self.P_y > 184)):
					self.fallset = 0
					self.P_y = self.ground
			elif (self.jumplevel == 2):
				self.ground = 260 - 96
				if((self.P_x < 270) & (self.P_x > 162) & (self.P_y > 144)):
					self.fallset = 0
					self.P_y = self.ground
			elif (self.jumplevel == 3):
				self.ground = 220 - 96
				if((self.P_x < 530) & (self.P_x > 362) & (self.P_y > 104)):
					self.fallset = 0
					self.P_y = self.ground
			elif (self.jumplevel == 4):
				self.ground = 180 - 96
				if((self.P_x < 490) & (self.P_x > 382) & (self.P_y > 64)):
					self.fallset = 0
					self.P_y = self.ground

		# 遇到障碍停止运动判定
		if stopup:
			self.Move_up = False
		if stopdown:
			self.Move_down = False
		if stopleft:
			self.Move_left = False
		if stopright:
			self.Move_right = False
		if (stopjump & (self.Move_jump != 0)):
			self.Move_jump = 0
			self.P_y = self.ground


# 雪花屏类
class Blank(pygame.sprite.Sprite):
	def __init__(self, start, flash):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([680, 10])
		self.image.fill((248, 248, 255))
		self.image.set_alpha(50)
		self.rect = pygame.draw.rect(
			self.image, (248, 248, 255), (0, start, 680, 10))
		self.mask = pygame.mask.from_surface(self.image)
		self.last_time = 0
		self.flash = flash

	def update(self, current_time, rate=2):
		if current_time > self.last_time + rate:
			self.rect.y += self.flash
			if(self.rect.y > 480):
				self.rect.y = 0
			self.last_time = current_time


# 地图墙类
class Wall(pygame.sprite.Sprite):
	def __init__(self, color, place):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([place[2], place[3]])
		self.image.fill(color)
		self.rect = pygame.draw.rect(self.image, color, place)
		self.mask = pygame.mask.from_surface(self.image)


# 第一卦地图
class Map1:
	def __init__(self):
		self.wallgroup = pygame.sprite.Group()
		self.wallgroup.add(Wall((0, 0, 0), (20, 0, 100, 160)))
		self.wallgroup.add(Wall((0, 0, 0), (20, 0, 270, 75)))
		self.wallgroup.add(Wall((0, 0, 0), (20, 240, 100, 190)))
		self.wallgroup.add(Wall((0, 0, 0), (20, 310, 270, 120)))
		self.wallgroup.add(Wall((0, 0, 0), (560, 0, 100, 160)))
		self.wallgroup.add(Wall((0, 0, 0), (380, 0, 270, 75)))
		self.wallgroup.add(Wall((0, 0, 0), (560, 240, 100, 190)))
		self.wallgroup.add(Wall((0, 0, 0), (380, 310, 270, 120)))

	# 向上障碍检测
	def checkup(self, x, y):
		if(y < 75 and y > 55 and (x < 280 or x > 340)):
			return True
		elif((x < 110 or x > 520) and (y < 160 and y > 140)):
			return True
		else:
			return False

	# 向下障碍检测
	def checkdown(self, x, y):
		if(y > 240 and y < 260 and (x < 280 or x > 340)):
			return True
		elif((x < 110 or x > 520) and y > 180 and y < 200):
			return True
		else:
			return False

	# 向左障碍检测
	def checkleft(self, x, y):
		if(x < 280 and x > 260 and (y < 75 or y > 220)):
			return True
		elif(x < 110 and x > 90 and (y < 140 or y > 180)):
			return True
		else:
			return False

	# 向右障碍检测
	def checkright(self, x, y):
		if(x > 340 and x < 360 and (y < 75 or y > 220)):
			return True
		elif(x > 520 and x < 540 and (y < 140 or y > 180)):
			return True
		else:
			return False

	# 游戏结束检测
	def gameovercheck(self, x, y):
		if(x < 40 and (y > 140 and y < 180)):
			return True
		elif(y > 340 and (x > 280 and x < 340)):
			return True
		elif(y < 30 and (x > 280 and x < 340)):
			return True
		else:
			return False


# 地图云类
class Cloud(pygame.sprite.Sprite):
	def __init__(self, color, place):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([place[2], place[3]])
		self.image.fill(color)
		self.rect = pygame.draw.rect(self.image, color, place)
		self.mask = pygame.mask.from_surface(self.image)


# 第二卦地图
class Map2:
	def __init__(self):
		self.cloudgroup1 = pygame.sprite.Group()
		self.cloudgroup1.add(Cloud((225, 225, 225), (180, 300, 60, 40)))
		self.cloudgroup1.add(Cloud((225, 225, 225), (200, 260, 80, 40)))
		self.cloudgroup1.add(Cloud((225, 225, 225), (260, 300, 60, 40)))
		self.cloudgroup2 = pygame.sprite.Group()
		self.cloudgroup1.add(Cloud((225, 225, 225), (400, 220, 60, 40)))
		self.cloudgroup1.add(Cloud((225, 225, 225), (420, 180, 80, 40)))
		self.cloudgroup1.add(Cloud((225, 225, 225), (480, 220, 60, 40)))
		self.allcloudgroup = pygame.sprite.Group()
		self.allcloudgroup.add(self.cloudgroup1)
		self.allcloudgroup.add(self.cloudgroup2)
		self.wallgroup = pygame.sprite.Group()
		self.wallgroup.add(Wall((225, 225, 225), (20, 0, 30, 400)))
		self.wallgroup.add(Wall((225, 225, 225), (630, 0, 30, 400)))
		self.wallgroup.add(Wall((225, 225, 225), (20, 390, 640, 30)))

		self.wallgroup.add(Wall((0, 0, 0), (20, 0, 100, 80)))
		self.wallgroup.add(Wall((0, 0, 0), (200, 0, 280, 80)))
		self.wallgroup.add(Wall((0, 0, 0), (560, 0, 100, 80)))
		self.wallgroup.add(Wall((0, 0, 0), (20, 400, 640, 30)))

	def checkjump(self, x, y):
		if((x < 270) & (x > 162) & (y < 160) & (y > 140)):
			return True
		if((x < 490) & (x > 382) & (y < 80) & (y > 60)):
			return True
		if((x < 310) & (x > 142) & (y < 200) & (y > 180)):
			return True
		if((x < 530) & (x > 362) & (y < 120) & (y > 100)):
			return True
		return False

	# 向左障碍检测
	def checkleft(self, x, y):
		if((y > 170) & (y < 300) & (x > 260) & (x < 280)):
			return True
		elif((y > 90) & (y < 220) & (x > 480) & (x < 500)):
			return True
		elif((y > 210) & (y < 340) & (x > 300) & (x < 320)):
			return True
		elif((y > 130) & (y < 260) & (x > 520) & (x < 540)):
			return True
		else:
			return False

	# 向右障碍检测
	def checkright(self, x, y):
		if((y > 170) & (y < 300) & (x > 152) & (x < 172)):
			return True
		elif((y > 90) & (y < 220) & (x > 372) & (x < 392)):
			return True
		elif((y > 210) & (y < 340) & (x > 132) & (x < 152)):
			return True
		elif((y > 130) & (y < 260) & (x > 352) & (x < 372)):
			return True
		else:
			return False

	def gameovercheck(self, x, y):
		return False


# 主程序
nowpath = sys.path[0] + "\\"  # 获取当前地址
pygame.init()  # pygame初始化
screen = pygame.display.set_mode((680, 480), 0, 32)
screen.fill([30, 144, 255])  # 创建屏幕
Stage = 1  # 关卡初始化
Gameover = False  # 游戏结束初始化
blankgroup = pygame.sprite.Group()  # 创建雪花屏
blankgroup.add(Blank(0, 60))
blankgroup.add(Blank(30, 50))
map = Map1()  # 创建地图为第一卦地图
pygame.display.set_caption("fight")  # 界面标题 TODO: 后期要改
framerate = pygame.time.Clock()  # 设置帧率
chara = Chara()  # 创建角色
chara.load("chara.png", 48, 96, 2)
charagroup = pygame.sprite.Group()
charagroup.add(chara)

# 第一卦开始
while (True):
	screen.fill([30, 144, 255])
	my_font = pygame.font.Font("font.ttf", 25)
	text_screen = my_font.render("0 0 0 0 0 0", False, (0, 0, 0))
	screen.blit(text_screen, (260, 450))
	map.wallgroup.draw(screen)
	time_passed = framerate.tick(30)

	time_passed_seconds = time_passed / 10.0
	ticks = pygame.time.get_ticks()

	chara.control(
		map.checkup(chara.P_x, chara.P_y),
		map.checkdown(chara.P_x, chara.P_y),
		map.checkleft(chara.P_x, chara.P_y),
		map.checkright(chara.P_x, chara.P_y),
		False)

	chara.move()
	charagroup.update(ticks)
	charagroup.draw(screen)
	blankgroup.update(ticks)
	blankgroup.draw(screen)
	if map.gameovercheck(chara.P_x, chara.P_y):
		Gameover = True
		chara.P_x = screen.get_width() / 2 - 48
		chara.P_y = screen.get_height() / 2 - 96
		chara.Move_up = False
		chara.Move_left = False
		chara.Move_right = False
		chara.speed = 10
		while (True):
			backtogame = False
			screen.fill([30, 144, 255])
			my_font = pygame.font.Font("font.ttf", 25)
			text_screen = my_font.render("0 0 0 0 0 0", False, (0, 0, 0))
			screen.blit(text_screen, (260, 450))
			map.wallgroup.draw(screen)
			time_passed = framerate.tick(30)
			time_passed_seconds = time_passed / 10.0
			ticks = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if(event.type == pygame.KEYDOWN):
					if(event.key == pygame.K_SPACE):
						backtogame = True
			if backtogame:
				chara.P_x = screen.get_width() / 2 - 48
				chara.P_y = screen.get_height() / 2 - 96
				chara.Move_down = False
				chara.speed = 4
				break

			chara.Move_down = True
			chara.move()
			if(chara.P_y > 360):
				chara.P_y = 0
			charagroup.update(ticks)
			charagroup.draw(screen)
			blankgroup.update(ticks)
			blankgroup.draw(screen)
			pygame.display.update()
	break
	if(chara.P_x > 580 and (chara.P_y > 140 and chara.P_y < 180)):
		break
	pygame.display.update()

# 第二卦开始
map = Map2()
Stage = 2
chara.P_x = screen.get_width() - 50 - 48
chara.P_y = 390 - 96
chara.Move_down = False
chara.Move_up = False
chara.Move_left = False
chara.Move_right = False
while True:
	screen.fill([30, 144, 255])
	my_font = pygame.font.Font("font.ttf", 25)
	text_screen = my_font.render("0 0 0 0 0 0", False, (0, 0, 0))
	screen.blit(text_screen, (260, 450))
	map.wallgroup.draw(screen)
	map.allcloudgroup.draw(screen)
	time_passed = framerate.tick(30)
	time_passed_seconds = time_passed / 10.0
	ticks = pygame.time.get_ticks()

	chara.control(
		False,
		False,
		map.checkleft(chara.P_x, chara.P_y),
		map.checkright(chara.P_x, chara.P_y),
		map.checkjump(chara.P_x, chara.P_y))

	chara.move()
	charagroup.update(ticks)
	charagroup.draw(screen)
	blankgroup.update(ticks)
	blankgroup.draw(screen)
	if(chara.P_y < 20 and (chara.P_x > 450 and chara.P_x < 560)):
		break
	pygame.display.update()

while True:
	screen.fill([30, 144, 255])
	my_font = pygame.font.Font("font.ttf", 25)
	text_screen = my_font.render("0 0 0 0 0 0", False, (0, 0, 0))
	screen.blit(text_screen, (260, 450))
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
	pygame.display.update()
