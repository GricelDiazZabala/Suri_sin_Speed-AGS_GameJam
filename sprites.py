import pygame
from config import *
import math
import random

class Spritesheet:
	def __init__(self, file):
		self.sheet = pygame.image.load(file).convert()

	def get_sprite(self, x, y, width, height):
		sprite = pygame.Surface([width, height])
		sprite.blit(self.sheet, (0,0), (x,y,width,height))
		sprite.set_colorkey(BLACK)
		return sprite

class Player(pygame.sprite.Sprite):
	
	def __init__(self, game, x, y):
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
            
		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE
		
		self.image = self.game.terrain_spritesheet.get_sprite(0,0, self.width, self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.x_change = 0
		self.y_change = 0

		self.facing = 'down'
		self.animation_loop = 1

		self.image = self.game.character_spritesheet.get_sprite(2, 8, self.width, self.height)

            
	def update(self):
		self.movement()
		self.animate()

		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')

		self.x_change = 0
		self.y_change = 0

	def movement(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			self.x_change -= PLAYER_SPEED
			self.facing = 'left'
		if keys[pygame.K_d]:
			self.x_change += PLAYER_SPEED
			self.facing = 'right'
		if keys[pygame.K_w]:
			self.y_change -= PLAYER_SPEED
			self.facing = 'up'
		if keys[pygame.K_s]:
			self.y_change += PLAYER_SPEED
			self.facing = 'down'

	def collide_blocks(self, direction):
		if direction == "x":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.x_change > 0:
					self.rect.x = hits[0].rect.left - self.rect.width
				if self.x_change < 0:
					self.rect.x = hits[0].rect.right
				
		if direction == "y":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.y_change > 0:
					self.rect.y = hits[0].rect.top - self.rect.height
				if self.y_change < 0:
					self.rect.y = hits[0].rect.bottom

	def animate(self):
		up_animations = [self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height),
				   self.game.character_spritesheet.get_sprite(27, 1, self.width, self.height),
				   self.game.character_spritesheet.get_sprite(59, 1, self.width, self.height),
				   self.game.character_spritesheet.get_sprite(1, 96, self.width, self.height)]
		
		right_animations = [self.game.character_spritesheet.get_sprite(1, 31, self.width, self.height),
					 self.game.character_spritesheet.get_sprite(28, 30, self.width, self.height),
					 self.game.character_spritesheet.get_sprite(59, 30, self.width, self.height),
					 self.game.character_spritesheet.get_sprite(96, 31, self.width, self.height)]

		left_animations = [self.game.character_spritesheet.get_sprite(1, 64, self.width, self.height),
					  self.game.character_spritesheet.get_sprite(29, 66, self.width, self.height),
					  self.game.character_spritesheet.get_sprite(60, 66, self.width, self.height),
					  self.game.character_spritesheet.get_sprite(97, 64, self.width, self.height)]

		down_animations = [self.game.character_spritesheet.get_sprite(1, 96, self.width, self.height),
					  self.game.character_spritesheet.get_sprite(30, 98, self.width, self.height),
					  self.game.character_spritesheet.get_sprite(61, 100, self.width, self.height),
					  self.game.character_spritesheet.get_sprite(94, 97, self.width, self.height)]

		if self.facing == "up":
			if self.y_change == 0:
				self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height)
			else:
				self.image = up_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "down":
			if self.y_change == 0:
				self.image = self.game.character_spritesheet.get_sprite(1, 96, self.width, self.height)
			else:
				self.image = down_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "right":
			if self.x_change == 0:
				self.image = self.game.character_spritesheet.get_sprite(1, 31, self.width, self.height)
			else:
				self.image = right_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

		if self.facing == "left":
			if self.x_change == 0:
				self.image = self.game.character_spritesheet.get_sprite(1, 64, self.width, self.height)
			else:
				self.image = left_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 4:
					self.animation_loop = 1

class Block(pygame.sprite.Sprite):
	def	__init__(self, game, x, y):
		self.game = game
		self._layer = BLOCK_LAYER
		self.groups = self.game.all_sprites, self.game.blocks
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		
class Ground(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = GROUND_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

class Button:
	def __init__(self, x, y, width, height, fg, bg, content, fontsize):
		self.font = pygame.font.SysFont('Arial', 30, bold=True, italic=False)
		self.content = content

		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.fg = fg
		self.bg = bg

		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.bg)
		self.rect = self.image.get_rect()

		self.rect.x = self.x
		self.rect.y = self.y

		self.text = self.font.render(self.content, True, self.fg)
		self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
		self.image.blit(self.text, self.text_rect)

	def is_pressed(self, pos, pressed):
		if self.rect.collidepoint(pos):
			if pressed[0]:
				return True
			return False
		return False