import pygame
from config import *
import math
import random

class Spritesheet:
	def __init__(self, file):
		self.sheet = pygame.image.load(file).convert()

	def get_sprite(self, x, y, width, height):
		sprite = pygame.Surface([width, height], pygame.SRCALPHA)
		sprite.blit(self.sheet, (0,0), (x,y,width,height))
		
		sprite = sprite.convert_alpha()
		
		for x_pixel in range(sprite.get_width()):
			for y_pixel in range(sprite.get_height()):
				color = sprite.get_at((x_pixel, y_pixel))
				if color == (0, 0, 0, 255) or color == (255, 255, 255, 255):
					sprite.set_at((x_pixel, y_pixel), (0, 0, 0, 0))
		
		return sprite

class Player(pygame.sprite.Sprite):

	
	def __init__(self, game, x, y):
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.inventory = {}
            
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

		self.health = 100
		self.last_attack = 0

	def update(self):
		self.movement()
		self.animate()

		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.collide_enemies()
		self.collide_items()
		self.rect.y += self.y_change
		self.collide_blocks('y')
		self.collide_enemies()
		self.collide_items()

		self.x_change = 0
		self.y_change = 0

		self.attack()
		#self.attackAnimation()
		self.check_level_complete()

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

	def collide_enemies(self):
		hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
		if hits:
			self.health -= 10
			if self.health <= 0:
				self.game.playing = False

	def collide_items(self):
		hits = pygame.sprite.spritecollide(self, self.game.items, True)
		if hits:
			for item in hits:
				print(f"Collected item at ({item.rect.x}, {item.rect.y})")
				if "items" not in self.inventory:
					self.inventory["items"] = 0
				self.inventory["items"] += 1

	def attack(self):
		keys = pygame.key.get_pressed()
		now = pygame.time.get_ticks()

		
		if keys[pygame.K_SPACE] and now - self.last_attack > ATTACK_COOLDOWN:
			self.last_attack = now
			
			if self.facing == 'up':
				Attack(self.game, self.rect.x, self.rect.y - TILESIZE)
			elif self.facing == 'down':
				Attack(self.game, self.rect.x, self.rect.y + TILESIZE)
			elif self.facing == 'left':
				Attack(self.game, self.rect.x - TILESIZE, self.rect.y)
			elif self.facing == 'right':
				Attack(self.game, self.rect.x + TILESIZE, self.rect.y)

	# def attackAnimation(self):
	# 	fire_animations = [self.game.suriAtq_spritesheet.get_sprite(26, 15, self.width, self.height),
	# 				 self.game.suriAtq_spritesheet.get_sprite(156, 15, self.width, self.height),
	# 				 self.game.suriAtq_spritesheet.get_sprite(281, 15, self.width, self.height),
	# 				 self.game.suriAtq_spritesheet.get_sprite(538, 15, self.width, self.height)]
		
	# 	self.image = self.game.character_spritesheet.get_sprite(1, 31, self.width, self.height)
	# 	self.image = fire_animations[math.floor(self.animation_loop)]
	# 	self.animation_loop += 0.1
	# 	if self.animation_loop >= 4:
	# 		self.animation_loop = 1

	def check_level_complete(self):
		if len(self.game.enemies) == 0 and len(self.game.items) == 0:
			self.game.level_up()

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

class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = ENEMY_LAYER
		self.groups = self.game.all_sprites, self.game.enemies
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.x_change = 0
		self.y_change = 0

		self.animation_loop = 1

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.direction = random.choice(['left', 'right', 'up', 'down'])
		self.move_counter = 0

	def update(self):
		self.auto_move()
		self.animate()
		
		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')

		self.x_change = 0
		self.y_change = 0

	def auto_move(self):
		if self.move_counter == 0:
			self.direction = random.choice(['left', 'right', 'up', 'down'])
			self.move_counter = random.randint(30, 90)

		if self.direction == 'left':
			self.x_change -= ENEMY_SPEED
		if self.direction == 'right':
			self.x_change += ENEMY_SPEED
		if self.direction == 'up':
			self.y_change -= ENEMY_SPEED
		if self.direction == 'down':
			self.y_change += ENEMY_SPEED

		self.move_counter -= 1

	def collide_blocks(self, direction):
		if direction == "x":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.x_change > 0:
					self.rect.x = hits[0].rect.left - self.rect.width
				if self.x_change < 0:
					self.rect.x = hits[0].rect.right
				self.direction = random.choice(['left', 'right', 'up', 'down'])
				self.move_counter = 0
				
		if direction == "y":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.y_change > 0:
					self.rect.y = hits[0].rect.top - self.rect.height
				if self.y_change < 0:
					self.rect.y = hits[0].rect.bottom
				self.direction = random.choice(['left', 'right', 'up', 'down'])
				self.move_counter = 0

	def animate(self):
		right_animations = [self.game.enemy_spritesheet.get_sprite(51, 55, self.width, self.height),
					 self.game.enemy_spritesheet.get_sprite(237, 55, self.width, self.height),
					 self.game.enemy_spritesheet.get_sprite(423, 55, self.width, self.height),
					 self.game.enemy_spritesheet.get_sprite(615, 55, self.width, self.height)]
		
		self.image = self.game.character_spritesheet.get_sprite(1, 31, self.width, self.height)
		self.image = right_animations[math.floor(self.animation_loop)]
		self.animation_loop += 0.1
		if self.animation_loop >= 4:
			self.animation_loop = 1

class Item(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = ITEM_LAYER
		self.groups = self.game.all_sprites, self.game.items
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = pygame.transform.scale(self.game.speed_img, (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

class Attack(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites, self.game.attacks
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x
		self.y = y
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.spawn_time = pygame.time.get_ticks()

	def update(self):
		hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
		
		if pygame.time.get_ticks() - self.spawn_time > 150:
			self.kill()

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

		self.image = self.game.props_spritesheet.get_sprite(36, 475, self.width, self.height)

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
	def __init__(self, x, y, width, height, fg, bg, content, font_size=30):
		self.font = pygame.font.SysFont('Arial', font_size, bold=True, italic=False)
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