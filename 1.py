# -*- coding: utf-8 -*-
import pygame

from sys import exit
from random import randint
from pygame.locals import *

global Stage
global time_passed_seconds


class Chara(pygame.sprite.Sprite):
	def __init__(self, target):
		pygame.sprite.Sprite.__init__(self)
		self.Move_jump = 0
		self.Move_left = False
		self.Move_right = False
		self.Move_up = False
		self.Move_down = False
		self.P_x = screen.get_width() / 2 - 48
		self.P_y = screen.get_height() / 2 - 96
		self.target_surface = target
		self.image = None
		self.master_image = None
		self.rect = None
		self.topleft = 0, 0
		self.frame = 0
		self.old_frame = -1
		self.frame_width = 1
		self.frame_height = 1
		self.first_frame = 0
		self.last_frame = 0
		self.columns = 1
		self.last_time = 0
		self.speed = 4

	def load(self, filename, width, height, columns):
		self.master_image = pygame.image.load(filename)
		self.frame_width = width
		self.frame_height = height
		self.rect = Rect(self.P_x, self.P_y, width, height)
		self.columns = columns
		rect = self.master_image.get_rect()
		self.last_frame = (rect.width // width) * (rect.height // height) - 1

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
			if(self.P_x <= (screen.get_width() - 48 - distance)):
				self.P_x += distance
		elif self.Move_right:
			if(self.P_x >= distance):
				self.P_x -= distance
		elif self.Move_up:
			if(self.P_y >= distance):
				self.P_y -= distance
		elif self.Move_down:
			if(self.P_y <= (screen.get_height() - 96 - distance)):
				self.P_y += distance

	def control(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				pygame.quit()
				exit()
			if(event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_d):
					self.Move_left = True
				if(event.key == pygame.K_a):
					self.Move_right = True
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
					self.Move_left = False
				if(event.key == pygame.K_a):
					self.Move_right = False
				if(Stage == 1):
					if(event.key == pygame.K_w):
						self.Move_up = False
					if(event.key == pygame.K_s):
						self.Move_down = False


class Wall(pygame.sprite.Sprite):
	def __init__(self, color, place, target):
		pygame.sprite.Sprite.__init__(self)
		self.target_surface = target
		self.image = pygame.Surface([place[2], place[3]])
		self.image.fill(color)
		self.rect = pygame.draw.rect(self.image, color, place)


pygame.init()
screen = pygame.display.set_mode((680, 480), 0, 32)
screen.fill([30, 144, 255])
framerate = pygame.time.Clock()
Stage = 1

wall1 = Wall((0, 0, 0), (20, 0, 100, 160), screen)
wall2 = Wall((0, 0, 0), (20, 0, 270, 75), screen)
wall3 = Wall((0, 0, 0), (20, 240, 100, 190), screen)
wall4 = Wall((0, 0, 0), (20, 310, 270, 120), screen)
wall5 = Wall((0, 0, 0), (560, 0, 100, 160), screen)
wall6 = Wall((0, 0, 0), (380, 0, 270, 75), screen)
wall7 = Wall((0, 0, 0), (560, 240, 100, 190), screen)
wall8 = Wall((0, 0, 0), (380, 310, 270, 120), screen)
wallgroup = pygame.sprite.Group()
wallgroup.add(wall1)
wallgroup.add(wall2)
wallgroup.add(wall3)
wallgroup.add(wall4)
wallgroup.add(wall5)
wallgroup.add(wall6)
wallgroup.add(wall7)
wallgroup.add(wall8)

chara = Chara(screen)
chara.load("chara.png", 48, 96, 2)
charagroup = pygame.sprite.Group()
charagroup.add(chara)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	screen.fill([30, 144, 255])
	time_passed = framerate.tick(30)
	time_passed_seconds = time_passed / 10.0
	ticks = pygame.time.get_ticks()
	wallgroup.update(ticks)
	wallgroup.draw(screen)
	chara.control()
	attacker = None
	attacker = pygame.sprite.spritecollideany(chara, wallgroup, collided=pygame.sprite.collide_rect)
	if attacker != None:
		if pygame.sprite.collide_rect_ratio(0.6)(chara, attacker):
			if chara.Move_up:
				chara.Move_up = False
			if chara.Move_down:
				chara.Move_down = False
			if chara.Move_left:
				chara.Move_left = False
			if chara.Move_right:
				chara.Move_right = False
	chara.move()
	charagroup.update(ticks)
	charagroup.draw(screen)
	pygame.display.update()


except BaseException:
	print(sys.exc_info())