import pygame

import random

import entities


# constants
FPS = 60
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
SCALE_FACTOR = 0.5
GROUND_HEIGHT = 20 * SCALE_FACTOR
LZ_WIDTH = 200 * SCALE_FACTOR
LZ_HEIGHT = 10 * SCALE_FACTOR
ROCKET_WIDTH = 20 * SCALE_FACTOR
ROCKET_HEIGHT = 80 * SCALE_FACTOR
THRESHOLD_LANDING_SPEED = 5
TITLE_TEXT_SIZE = 48
TEXT_SIZE = 24
NUM_IN_GENERATION = 50

# colours
SKY_BLUE = (50, 150, 240)
PLAY_YELLOW = (240, 240, 40)
TRAIN_PURPLE = (240, 40, 240)
GROUND_GREEN = (100, 250, 120)
LZ_RED = (250, 100, 100)
ROCKET_WHITE = (255, 255, 255)
TITLE_TEXT_COLOUR = (255, 255, 255)
TEXT_COLOUR = (255, 255, 255)

# start pygame, set the title, and make the window
pygame.init()
pygame.display.set_caption("Rocket Game")
background = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# the main menu
def menu():
	# set font for menu
	font = pygame.font.SysFont('Comic Sans MS', TITLE_TEXT_SIZE)

	# make the play and train buttons
	play_button = entities.Button((WINDOW_WIDTH - BUTTON_WIDTH) / 2,\
		WINDOW_HEIGHT / 2 - 1.1 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
	train_button = entities.Button((WINDOW_WIDTH - BUTTON_WIDTH) / 2,\
		WINDOW_HEIGHT / 2, BUTTON_WIDTH, BUTTON_HEIGHT)

	# menu control variables
	in_menu = True
	choice = None

	while in_menu:
		# reset the background
		background.fill(SKY_BLUE)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# detect exit button clicked
				choice = 'exit'
				in_menu = False
			if event.type == pygame.MOUSEBUTTONDOWN:	# detect mouse clicks
				mouse_position = event.pos
				if play_button.collidepoint(mouse_position):	# mouse clicked on play button
					choice = 'play'
					in_menu = False 
				elif train_button.collidepoint(mouse_position):		# mouse clicked on train button
					choice = 'train'
					in_menu = False

		# draw the buttons
		pygame.draw.rect(background, PLAY_YELLOW, play_button)
		pygame.draw.rect(background, TRAIN_PURPLE, train_button)

		# draw the menu text
		display_text(font, "Click yellow to play, or purple to train!",\
			(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 2 * BUTTON_HEIGHT), TITLE_TEXT_COLOUR, centered = True)

		pygame.display.update()

	# return the choice from the menu
	return choice


# play the game!
def play():
	font = pygame.font.SysFont('Comic Sans MS', TEXT_SIZE)
	clock = pygame.time.Clock()

	# make the initial entities
	ground = entities.Ground(0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT)
	lz = entities.LandingZone((WINDOW_WIDTH - LZ_WIDTH) / 2, WINDOW_HEIGHT - GROUND_HEIGHT - LZ_HEIGHT, LZ_WIDTH, LZ_HEIGHT)
	#rocket = entities.Rocket((WINDOW_WIDTH - ROCKET_WIDTH) / 2, 0, ROCKET_WIDTH, ROCKET_HEIGHT)
	rocket = entities.Rocket(random.randint(0, WINDOW_WIDTH - ROCKET_WIDTH), 0, ROCKET_WIDTH, ROCKET_HEIGHT)

	playing = True
	rocket_finished = False

	while playing:
		# play at a limited FPS
		dt = clock.tick(FPS) / 1000

		# refresh the background
		background.fill(SKY_BLUE)

		# determine if the user wants to exit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False

		# handle keyboard input to rocket
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			rocket.move_up(background)
			output = [1, 0, 0]
		elif keys[pygame.K_RIGHT]:
			rocket.move_right(background)
			output = [0, 1, 0]
		elif keys[pygame.K_LEFT]:
			rocket.move_left(background)
			output = [0, 0, 1]
		elif keys[pygame.K_ESCAPE]:
			playing = False

		# draw entities to background
		pygame.draw.rect(background, GROUND_GREEN, ground)
		pygame.draw.rect(background, LZ_RED, lz)
		pygame.draw.rect(background, ROCKET_WHITE, rocket)

		# change position of rocket
		rocket.update(dt)

		# check for collision
		if rocket.colliderect(lz):
			if rocket.y_velocity < THRESHOLD_LANDING_SPEED:
				rocket.stop(exploded = False)
				display_text(font, "You landed safely! Press ESC to go to menu.", 'center', TEXT_COLOUR)
			else:
				rocket.stop(exploded = True)
				display_text(font, "You hit the landing zone too hard! Press ESC to go to menu.", 'center', TEXT_COLOUR)
		elif rocket.colliderect(ground):
			rocket.stop(exploded = True)
			display_text(font, "You missed the landing zone! Press ESC to go to menu.", 'center', TEXT_COLOUR)
		elif rocket.x > WINDOW_WIDTH - ROCKET_WIDTH or rocket.x < 0 or rocket.y < -100:
			rocket.stop(exploded = True)
			display_text(font, "You went the wrong way! Press ESC to go to menu.", 'center', TEXT_COLOUR)

		# display relevant data
		display_text(font, "Vertical speed: " + str(round(-rocket.y_velocity, 1)), (10, 10), TEXT_COLOUR)
		display_text(font, "Horizontal speed: " + str(rocket.x_velocity), (10, 10 + TEXT_SIZE), TEXT_COLOUR)
		display_text(font, "Vertical distance above LZ: " + str(lz.y - (rocket.y + ROCKET_HEIGHT)),\
			(10, 10 + 2 * TEXT_SIZE), TEXT_COLOUR)
		display_text(font, "Horizontal distance between LZ center: "\
			+ str((rocket.x + ROCKET_WIDTH / 2) - (lz.x + LZ_WIDTH / 2)), (10, 10 + 3 * TEXT_SIZE), TEXT_COLOUR)
		display_text(font, "Fuel: " + str(rocket.fuel), (10, 10 + 4 * TEXT_SIZE), TEXT_COLOUR)

		pygame.display.update()


# train rockets using an evolution algorithm
def gen_train():
	font = pygame.font.SysFont('Comic Sans MS', TEXT_SIZE)
	clock = pygame.time.Clock()

	# make the initial entities
	ground = entities.Ground(0, WINDOW_HEIGHT - GROUND_HEIGHT, WINDOW_WIDTH, GROUND_HEIGHT)
	lz = entities.LandingZone((WINDOW_WIDTH - LZ_WIDTH) / 2, WINDOW_HEIGHT - GROUND_HEIGHT - LZ_HEIGHT, LZ_WIDTH, LZ_HEIGHT)

	# training control variables
	training = True
	generation = 1

	# store the starting x and y positions
	start_x = random.randint(0, WINDOW_WIDTH - ROCKET_WIDTH)
	start_y = 0

	while training:
		# list to hold the rockets in this generation
		rockets = []

		# fill the rockets list
		for i in range(NUM_IN_GENERATION):
			rocket = entities.GenerationRocket(start_x, start_y, ROCKET_WIDTH, ROCKET_HEIGHT)
			if generation == 1:
				# rockets with random weights
				rocket.initialize_moves(moves = 'random')
			else:
				# rockets with evolved weights
				rocket.initialize_moves(moves = new_moves[i])
			rockets.append(rocket)

		# assign a variable to hold the number of rockets still moving in the generation
		num_left = len(rockets)

		# assign a variable to hold the number of rockets that landed safely
		safe_landings = 0

		while num_left > 0:
			# play at a limited FPS
			dt = clock.tick(FPS) / 1000

			# refresh the background
			background.fill(SKY_BLUE)

			# loop through the rockets to update each one
			for rocket in rockets:
				# determine if the user wants to exit
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						training = False
						num_left = 0

				# handle keyboard input to rocket
				keys = pygame.key.get_pressed()
				if keys[pygame.K_ESCAPE]:
					training = False
					num_left = 0

				# get rocket position and velocity data used to update the rocket's score
				data = [(rocket.x + ROCKET_WIDTH / 2) - (lz.x + LZ_WIDTH / 2),\
					lz.y - (rocket.y + ROCKET_HEIGHT), rocket.x_velocity, rocket.y_velocity, rocket.fuel]
				rocket.update_score(data)

				# move and update the rocket
				rocket.move(background)
				rocket.update(dt)

				if not rocket.stopped:
					# check for collisions
					if rocket.colliderect(lz):
						if rocket.y_velocity < THRESHOLD_LANDING_SPEED:
							rocket.stop(exploded = False)
							rocket.min_score += -1000
							num_left -= 1
							safe_landings += 1
						else:
							rocket.stop(exploded = True)
							num_left -= 1
					elif rocket.colliderect(ground):
						rocket.stop(exploded = True)
						num_left -= 1
					elif rocket.x > WINDOW_WIDTH - ROCKET_WIDTH or rocket.x < 0 or rocket.y < -100:
						rocket.stop(exploded = True)
						num_left -= 1

				# draw the rocket to the background
				pygame.draw.rect(background, ROCKET_WHITE, rocket)

			# draw the other entities to the background
			pygame.draw.rect(background, GROUND_GREEN, ground)
			pygame.draw.rect(background, LZ_RED, lz)

			# display generation information
			display_text(font, "Press ESC to exit.", (10, 10), TEXT_COLOUR)
			display_text(font, "Generation #" + str(generation), (10, 10 + TEXT_SIZE), TEXT_COLOUR)
			display_text(font, "Number of rockets left: " + str(num_left), (10, 10 + 2 * TEXT_SIZE), TEXT_COLOUR)
			display_text(font, "Number of safe landings in generation: " + str(safe_landings),\
				(10, 10 + 3 * TEXT_SIZE), TEXT_COLOUR)
			if generation > 1:
				display_text(font, "Average score of generation #" + str(generation - 1) + ": "\
					+ str(round(mean_score, 3)), (10, 10 + 4 * TEXT_SIZE), TEXT_COLOUR)

			pygame.display.update()


		# sort the rockets list based on their score
		rockets.sort(key = lambda x: x.min_score, reverse = False)

		# get the sorted scores as a list
		sorted_scores = [rocket.min_score for rocket in rockets]

		# calculate the mean score of this generation
		mean_score = sum(sorted_scores) / len(sorted_scores)

		# identify the moves of each rocket in order from best to worst
		sorted_moves = [rocket.moves for rocket in rockets]

		# evolve these moves to get better rockets
		new_moves = evolve(sorted_moves)

		generation += 1


# evolve the moves for training
def evolve(sorted_weights):
	return_moves = []
	best_rocket = sorted_weights[0]
	second_best_rocket = sorted_weights[1]
	num_moves = len(best_rocket)

	for rocket_number in range(NUM_IN_GENERATION):
		current_moves = []
		if rocket_number < 2:	# save the best two rockets for the next generation
			current_moves = sorted_weights[rocket_number]
		elif rocket_number < NUM_IN_GENERATION - 0:		# make all other rockets of the next generation from the best rockets
			for move in range(num_moves):	# loop through each move
				# decide whether to replace the current move with one from the second best rocket
				crossover = random.getrandbits(1)

				# decide whether to mutate the current move
				mutate = True if random.random() < 0.05 else False

				# have a variable store the current move
				current_move = 0

				# either replace or keep the move
				if crossover:
					current_move = second_best_rocket[move]
					#current_moves.append(second_best_rocket[move])
				else:
					current_move = best_rocket[move]
					#current_moves.append(best_rocket[move])

				if mutate:
					# add or subtract one to the move
					current_move += random.choice([-1, 1])

				current_moves.append(current_move)
		else:	# CURRENTLY NOT USED
			# make a list of completely random moves
			for move in range(num_moves):
				current_moves.append(random.randint(0, 2))

		return_moves.append(current_moves)

	return return_moves


# display text without a hassle
def display_text(font, text, position, colour, centered = False):
	# get the textview to do some positioning if needed
	text_view = font.render(text, True, colour)
	if position == 'center':	# position in center of screen
		background.blit(text_view, ((WINDOW_WIDTH - text_view.get_rect().width) / 2, WINDOW_HEIGHT / 2))
	elif not centered:	# position the top left according to the position argument
		background.blit(text_view, position)
	else:	# position the center at the position argument
		background.blit(text_view, (position[0] - text_view.get_rect().width / 2,\
			position[1] - text_view.get_rect().height / 2))


if __name__ == "__main__":
	while True:
		choice = menu()

		if choice == 'play':	# play the game
			play()
		elif choice == 'train':		# watch the generations evolve
			gen_train()
		elif choice == 'exit':	# exit the game
			break

	pygame.quit()




