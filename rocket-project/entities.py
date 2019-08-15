import pygame
import numpy as np
import random


class Button(pygame.Rect):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)

class Ground(pygame.Rect):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)

class LandingZone(pygame.Rect):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)

class Rocket(pygame.Rect):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)
		self.y_velocity = 0
		self.x_velocity = 0
		self.thrust_velocity = 0.5
		self.side_velocity = 0.5
		self.stopped = False
		self.starting_fuel = 100
		self.fuel = self.starting_fuel
		self.flame_width = 4
		self.flame_height = 8
		self.flame_colour = (255, 158, 30)

	def move_up(self, background):
		if not self.stopped and self.fuel > 0:
			self.y_velocity -= self.thrust_velocity
			self.fuel -= 1
			# draw the flame
			pygame.draw.rect(background, self.flame_colour, (self.x + (self.width - 4) / 2,\
				self.y + self.height, self.flame_width, self.flame_height))

	def move_right(self, background):
		if not self.stopped and self.fuel > 0:
			self.x_velocity += self.side_velocity
			self.fuel -= 1
			# draw the flame
			pygame.draw.rect(background, self.flame_colour, (self.x - self.flame_height,\
				self.y + (self.height - self.flame_width) / 2, self.flame_height, self.flame_width))

	def move_left(self, background):
		if not self.stopped and self.fuel > 0:
			self.x_velocity -= self.side_velocity
			self.fuel -= 1
			# draw the flame
			pygame.draw.rect(background, self.flame_colour, (self.x + self.width,\
				self.y + (self.height - self.flame_width) / 2, self.flame_height, self.flame_width))

	def update(self, dt):
		if not self.stopped:
			self.y_velocity += 4 * dt

			self.x += self.x_velocity
			self.y += self.y_velocity

	def stop(self, exploded):
		self.stopped = True
		if exploded:
			pass
			#print("Boom")

# wants to get the LOWEST score
class GenerationRocket(Rocket):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height)
		self.starting_fuel = 1000
		self.fuel = self.starting_fuel
		self.move_number = 0
		self.current_score = 0
		self.min_score = 1000000

	def initialize_moves(self, moves = 'random'):
		# initialize moves based on function parameter
		if moves == 'random':	# init random moves
			self.moves = [random.randint(0, 2) for i in range(self.starting_fuel)]
		else:	# init as parameter moves
			self.moves = moves

	def move(self, background):
		move = -1 if self.move_number >= self.starting_fuel else self.moves[self.move_number]
		if move == 0:
			# move up
			self.move_up(background)
		elif move == 1:
			# move right
			self.move_right(background)
		elif move == 2:
			# move left
			self.move_left(background)
		else:
			# no thrust in any direction
			pass
		self.move_number += 1

	def update_score(self, data):
		# reset the current score
		self.current_score = 0

		# calculate the current score
		for i in range(len(data)):
			if i < len(data) - 1:
				self.current_score += data[i] ** 2	# position and velocity data are squared and added => higher score
			else:
				self.current_score -= data[i]	# the last element (fuel) is subtracted => more fuel, lower score

		# determine if the current score is less than the minimum score
		if self.current_score < self.min_score:
			self.min_score = self.current_score









