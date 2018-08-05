# -*- coding: utf-8 -*-

import math
import pygame
from pygame.locals import *
from sys import exit
import sys

global Stage
global time_passed_seconds


class Chara(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.Move_jump = 0
		self.Move_left = False
		self.Move_right = False
		self.Move_up = False
		self.Move_down = False
		self.P_x = screen.get_width() / 2 - 48
		self.P_y = screen.get_height() / 2 - 96
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
		self.direction = 0
		self.speed = 4

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
		self.rect = Rect(self.P_x, self.P_y, self.frame_width, self.frame_height)

	def move(self):
		distance = self.speed * time_passed_seconds

		if (self.Move_jump == 1) & (self.P_y == 150):
			self.P_y -= distance
		elif (self.Move_jump == 1) & (150 > self.P_y > 90):
			self.P_y -= distance
		elif self.P_y == 90:
			self.Move_jump = 2
			self.P_y += distance
		elif (self.Move_jump == 2) & (150 > self.P_y > 90):
			self.P_y += distance
		elif (self.Move_jump == 2) & (150 == self.P_y):
			self.Move_jump = 0

		elif self.Move_left:
			if(self.P_x >= distance):
				self.P_x -= distance

		elif self.Move_right:
			if(self.P_x <= (screen.get_width() - 48 - distance)):
				self.P_x += distance

		elif self.Move_up:
			if(self.P_y >= distance):
				self.P_y -= distance

		elif self.Move_down:
			if(self.P_y <= (screen.get_height() - 96 - distance)):
				self.P_y += distance

	def control(self, stopup, stopdown, stopleft, stopright):
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				exit()
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_d):
					self.Move_right = True
				if(event.key == pygame.K_a):
					self.Move_left = True
				if(Stage == 2):
					if(event.key == pygame.K_w) & (self.Move_jump == 0):
						self.Move_jump = 1
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
		if stopup:
			self.Move_up = False
		if stopdown:
			self.Move_down = False
		if stopleft:
			self.Move_left = False
		if stopright:
			self.Move_right = False


class Blank(pygame.sprite.Sprite):
	def __init__(self, start, flash):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([680, 10])
		self.image.fill((248, 248, 255))
		self.image.set_alpha(50)
		self.rect = pygame.draw.rect(self.image, (248, 248, 255), (0, start, 680, 10))
		self.mask = pygame.mask.from_surface(self.image)
		self.last_time = 0
		self.flash = flash

	def update(self, current_time, rate=2):
		if current_time > self.last_time + rate:
			self.rect.y += self.flash
			if(self.rect.y > 480):
				self.rect.y = 0
			self.last_time = current_time


class Wall(pygame.sprite.Sprite):
	def __init__(self, color, place):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([place[2], place[3]])
		self.image.fill(color)
		self.rect = pygame.draw.rect(self.image, color, place)
		self.mask = pygame.mask.from_surface(self.image)


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

	def checkup(self, x, y):
		if(y < 75 and (x < 280 or x > 340)):
			return True
		elif((x < 110 or x > 520) and y < 160):
			return True
		else:
			return False

	def checkdown(self, x, y):
		if(y > 240 and (x < 280 or x > 340)):
			return True
		elif((x < 110 or x > 520) and y > 180):
			return True
		else:
			return False

	def checkleft(self, x, y):
		if(x < 280 and (y < 75 or y > 220)):
			return True
		elif(x < 110 and (y < 140 or y > 180)):
			return True
		else:
			return False

	def checkright(self, x, y):
		if(x > 340 and (y < 75 or y > 220)):
			return True
		elif(x > 520 and (y < 140 or y > 180)):
			return True
		else:
			return False

	def gameovercheck(self, x, y):
		if(x < 40 and (y > 140 and y < 180)):
			return True
		elif(y > 280 and (x > 280 and x < 340)):
			return True
		elif(y < 30 and (x > 280 and x < 340)):
			return True
		else:
			return False


nowpath = sys.path[0] + "\\"
pygame.init()
screen = pygame.display.set_mode((680, 480), 0, 32)
screen.fill([30, 144, 255])
Stage = 1
Gameover = False
blankgroup = pygame.sprite.Group()
blankgroup.add(Blank(0, 60))
blankgroup.add(Blank(30, 50))
map = Map1()
pygame.display.set_caption("fight")
framerate = pygame.time.Clock()
chara = Chara()
chara.load("chara.png", 48, 96, 2)
charagroup = pygame.sprite.Group()
charagroup.add(chara)
while (True):

	screen.fill([30, 144, 255])
	map.wallgroup.draw(screen)
	time_passed = framerate.tick(30)
	time_passed_seconds = time_passed / 10.0
	ticks = pygame.time.get_ticks()

	chara.control(
		map.checkup(chara.P_x, chara.P_y),
		map.checkdown(chara.P_x, chara.P_y),
		map.checkleft(chara.P_x, chara.P_y),
		map.checkright(chara.P_x, chara.P_y))

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
			if(chara.P_y > 370):
				chara.P_y = 0
			charagroup.update(ticks)
			charagroup.draw(screen)
			blankgroup.update(ticks)
			blankgroup.draw(screen)
			pygame.display.update()

	if(chara.P_x > 580 and (chara.P_y > 140 and chara.P_y < 180)):
		break
	pygame.display.update()


while True:
	screen.fill([30, 144, 255])
	my_font = pygame.font.SysFont(None, 22)
	text_screen = my_font.render("finish first stage", True, (255, 0, 0))
	screen.blit(text_screen, (50, 50))
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
	pygame.display.update()
