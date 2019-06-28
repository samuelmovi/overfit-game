import pygame
from pygame.locals import *


FPS = 30  # frames per second to update the screen
W_WIDTH = 800  # width of the program's window, in pixels
W_HEIGHT = 600  # height in pixels


class MyButton(pygame.sprite.Sprite):
	rect = None
	surface = None

	def __init__(self, font, text, text_color, bg_color):
		self.surface = font.render(text, True, text_color, bg_color)
		self.rect = self.surface.get_rect()

	def set_coords(self, x, y):
		self.rect.center = (x, y)


class InputBox:

	def __init__(self, x, y, w, h, text=''):
		self.SMALLFONT = pygame.font.Font('freesansbold.ttf', 22)
		self.rect = pygame.Rect(x, y, w, h)
		grey = (100, 100, 100)
		self.color = grey
		self.text = text
		self.txt_surface = self.SMALLFONT.render(self.text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			# If the user clicked on the input_box rect.
			if self.rect.collidepoint(event.pos):
				# Toggle the active variable.
				self.active = not self.active
			else:
				self.active = False
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_BACKSPACE:
					if len(self.text) > 0:
						self.text = self.text[:-1]
						print("[#] Removing last character from input box: {}".format(self.text))
						self.txt_surface = self.SMALLFONT.render(self.text, True, (0, 0, 0))
				else:
					self.text += event.unicode
					print("[#] adding character to input box: {}".format(self.text))
				# Re-render the text.
				self.txt_surface = self.SMALLFONT.render(self.text, True, self.color)

	def update(self):
		# Resize the box if the text is too long.
		width = max(200, self.txt_surface.get_width()+10)
		self.rect.w = width

	def draw(self, screen):
		# blackout box
		pygame.draw.rect(screen, (0, 0, 0), self.rect, 0)
		# Blit the rect.
		pygame.draw.rect(screen, self.color, self.rect, 2)
		# Blit the text.
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

	def get_text(self):
		return self.text


class MyView:
	#       R   G   B
	GREY = (100, 100, 100)
	# NAVYBLUE = ( 60, 60, 100)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	# BLUE = ( 0,0, 255)
	YELLOW = (255, 255, 0)
	ORANGE = (255, 128, 0)
	# PURPLE = (255,0, 255)
	# CYAN = ( 0, 255, 255)
	BLACK = (0, 0, 0)

	def __init__(self):
		print('[#] Initiating View...')
		self.screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
		self.SMALLFONT = pygame.font.Font('freesansbold.ttf', 22)
		self.MEDIUMFONT = pygame.font.Font('freesansbold.ttf', 28)
		self.BIGFONT = pygame.font.Font('freesansbold.ttf', 34)

		self.ball = pygame.image.load('resources/ball.png')
		self.triangle_full = pygame.image.load('resources/triangle-pink-full.png')
		self.triangle_empty = pygame.image.load('resources/triangle-pink-empty.png')
		self.square_full = pygame.image.load('resources/square-yellow-full.png')
		self.square_empty = pygame.image.load('resources/square-yellow-empty.png')
		self.triangle_hole_complete = pygame.image.load('resources/triangle-hole-green-complete.png')
		self.triangle_hole_full = pygame.image.load('resources/triangle-hole-green-full.png')
		self.triangle_hole_empty = pygame.image.load('resources/triangle-hole-green-empty.png')
		self.square_hole_complete = pygame.image.load('resources/square-hole-red-complete.png')
		self.square_hole_full = pygame.image.load('resources/square-hole-red-full.png')
		self.square_hole_empty = pygame.image.load('resources/square-hole-red-empty.png')
		self.player_full = pygame.image.load('resources/player-full.png')
		self.player_empty = pygame.image.load('resources/player-empty.png')

		self.fire1 = pygame.image.load('resources/fire1.png')
		self.fire2 = pygame.image.load('resources/fire2.png')
		self.fire3 = pygame.image.load('resources/fire3.png')

		self.ray = pygame.image.load('resources/ray-short.png')

	# DISPLAY-DRAWING FUNCTIONS
	def draw_start_screen(self):
		self.screen.fill(self.BLACK)
		welcome_button = MyButton(self.BIGFONT, 'Welcome to WeeriMeeris', self.BLACK, self.GREEN)
		welcome_button.set_coords(W_WIDTH/2, 100)

		single_player_button = MyButton(self.MEDIUMFONT, 'Single Player', self.RED, self.YELLOW)
		single_player_button.set_coords(W_WIDTH/2, W_HEIGHT/2)

		online_multi_button = MyButton(self.MEDIUMFONT, 'Online Multiplayer', self.RED, self.YELLOW)
		online_multi_button.set_coords(W_WIDTH/2, W_HEIGHT/2 + 50)

		settings_button = MyButton(self.MEDIUMFONT, 'Settings', self.RED, self.ORANGE)
		settings_button.set_coords(W_WIDTH/2, W_HEIGHT/2 + 150)

		self.screen.fill(self.BLACK)
		self.screen.blit(welcome_button.surface, welcome_button.rect)
		self.screen.blit(single_player_button.surface, single_player_button.rect)
		self.screen.blit(online_multi_button.surface, online_multi_button.rect)
		self.screen.blit(settings_button.surface, settings_button.rect)

		return single_player_button, online_multi_button, settings_button

	def draw_game_board(self, player):
		self.screen.fill(self.BLACK)
		# draw boundary lines
		pygame.draw.line(self.screen, self.WHITE, (150, 0), (150, W_HEIGHT), 4)
		pygame.draw.line(self.screen, self.WHITE, (0, 300), (150, 300), 4)
		for n in range(7):
			pygame.draw.line(self.screen, self.WHITE, (150+90*n, 0), (150+90*n, W_HEIGHT-100), 4)
		# player 1 score board
		# draw player name
		player_name = MyButton(self.MEDIUMFONT, player.name, self.WHITE, self.GREY)
		player_name.set_coords(75, 25)
		self.screen.blit(player_name.surface, player_name.rect)
		# draw player score
		player_score_title = MyButton(self.SMALLFONT, 'SCORE', self.RED, self.BLACK)
		player_score_title.set_coords(75, 65)
		self.screen.blit(player_score_title.surface, player_score_title.rect)
		player_score = MyButton(self.BIGFONT, format(player.score), self.RED, self.BLACK)
		player_score.set_coords(75, 105)
		self.screen.blit(player_score.surface, player_score.rect)
		# draw total number of figures at play
		player_total_title = MyButton(self.SMALLFONT, 'TOTAL', self.GREEN, self.BLACK)
		player_total_title.set_coords(75, 145)
		self.screen.blit(player_total_title.surface, player_total_title.rect)
		player_total_title = MyButton(self.BIGFONT, format(player.total), self.GREEN, self.BLACK)
		player_total_title.set_coords(75, 185)
		self.screen.blit(player_total_title.surface, player_total_title.rect)
		# draw occupancy of the most occupied column
		player_longest_title = MyButton(self.SMALLFONT, 'LONGEST', self.YELLOW, self.BLACK)
		player_longest_title.set_coords(75, 225)
		self.screen.blit(player_longest_title.surface, player_longest_title.rect)
		player_longest_title = MyButton(self.BIGFONT, format(player.longest), self.YELLOW, self.BLACK)
		player_longest_title.set_coords(75, 265)
		self.screen.blit(player_longest_title.surface, player_longest_title.rect)

	def draw_online_options_screen(self, player_name, ip):
		banner = self.BIGFONT.render('   SETTINGS   ', 1, self.BLACK, self.GREEN)
		banner_rect = banner.get_rect()
		banner_rect.center = (W_WIDTH / 2, 100)

		host = self.SMALLFONT.render('Online Host', 1, self.GREEN, self.GREY)
		host_rect = host.get_rect()
		host_rect.center = (W_WIDTH / 2 - 100, 175)
		host_input = InputBox(W_WIDTH / 2 + 25, 160, 150, 30, ip)

		name = self.SMALLFONT.render('Player Name', 1, self.GREEN, self.GREY)
		name_rect = name.get_rect()
		name_rect.center = (W_WIDTH / 2 - 100, 225)
		name_input = InputBox(W_WIDTH / 2 + 25, 210, 150, 30, player_name)

		start_multi_button = MyButton(self.MEDIUMFONT, 'Online Multiplayer', self.RED, self.YELLOW)
		start_multi_button.set_coords(W_WIDTH / 2, W_HEIGHT / 2 + 50)

		inputs = (host_input, name_input)

		self.screen.fill(self.BLACK)
		self.screen.blit(banner, banner_rect)
		self.screen.blit(host, host_rect)
		self.screen.blit(name, name_rect)
		self.refresh_input(inputs)
		self.screen.blit(start_multi_button.surface, start_multi_button.rect)

		return inputs, start_multi_button

	def draw_settings_screen(self, player_name, ip):
		banner = self.BIGFONT.render('   SETTINGS   ', 1, self.BLACK, self.GREEN)
		banner_rect = banner.get_rect()
		banner_rect.center = (W_WIDTH/2, 100)

		host = self.SMALLFONT.render('Online Host', 1, self.GREEN, self.GREY)
		host_rect = host.get_rect()
		host_rect.center = (W_WIDTH/2-100, 175)
		host_input = InputBox(W_WIDTH/2+25, 160, 150, 30, ip)

		name = self.SMALLFONT.render('Player Name', 1, self.GREEN, self.GREY)
		name_rect = name.get_rect()
		name_rect.center = (W_WIDTH / 2 - 100, 225)
		name_input = InputBox(W_WIDTH/2+25, 210, 150, 30, player_name)

		save_button = MyButton(self.MEDIUMFONT, 'Save', self.RED, self.YELLOW)
		save_button.set_coords(W_WIDTH / 2, W_HEIGHT / 2 + 50)

		inputs = (host_input, name_input)

		self.screen.fill(self.BLACK)
		self.screen.blit(banner, banner_rect)
		self.screen.blit(host, host_rect)
		self.screen.blit(name, name_rect)
		self.refresh_input(inputs)
		self.screen.blit(save_button.surface, save_button.rect)

		return inputs, save_button

	def draw_wait_screen(self, text='  WAITING FOR AVAILABLE ONLINE PLAYER  '):
		banner = MyButton(self.BIGFONT, text, self.GREEN, self.BLACK)
		banner.set_coords(W_WIDTH/2, 200)

		dots = MyButton(self.BIGFONT, '...', self.GREEN, self.BLACK)
		dots.set_coords(W_WIDTH/2, 300)

		self.screen.fill(self.BLACK)
		self.screen.blit(banner.surface, banner.rect)
		self.screen.blit(dots.surface, dots.rect)

	def refresh_input(self, inputs):
		for instance in inputs:
			instance.update()
			instance.draw(self.screen)

	def draw_figures(self, columns):
		image = None
		x = 90
		for n in range(7):
			x += 90
			y = 0
			for figure in columns[n].figures:
				y += 50
				if figure.shape == 'ball':
					image = self.ball
				elif figure.shape == 'triangle':
					if figure.value == 2:
						image = self.triangle_empty
					elif figure.value == 3:
						image = self.triangle_full
				elif figure.shape == 'square':
					if figure.value == 2:
						image = self.square_empty
					elif figure.value == 3:
						image = self.square_full
				elif figure.shape == 'triangle-hole':
					if figure.value == 3:
						image = self.triangle_hole_empty
					elif figure.value == 5:
						image = self.triangle_hole_full
					elif figure.value == 6:
						image = self.triangle_hole_complete
				elif figure.shape == 'square-hole':
					if figure.value == 3:
						image = self.square_hole_empty
					elif figure.value == 5:
						image = self.square_hole_full
					elif figure.value == 6:
						image = self.square_hole_complete

				self.screen.blit(image, (x, y))

	def draw_player(self, player):
		if player.status == 'full':
			image = self.player_full
		else:
			image = self.player_empty
		self.screen.blit(image, (player.position*90+175, 525))

	def draw_opponent(self, opponent):
		# draw opponent name
		player_name = MyButton(self.MEDIUMFONT, opponent['name'], self.WHITE, self.GREY)
		player_name.set_coords(75, 325)
		self.screen.blit(player_name.surface, player_name.rect)
		# draw opponent score
		player_score_title = MyButton(self.SMALLFONT, 'SCORE', self.RED, self.BLACK)
		player_score_title.set_coords(75, 365)
		self.screen.blit(player_score_title.surface, player_score_title.rect)
		player_score = MyButton(self.BIGFONT, str(opponent['score']), self.RED, self.BLACK)
		player_score.set_coords(75, 405)
		self.screen.blit(player_score.surface, player_score.rect)
		# draw total number of figures at play
		player_total_title = MyButton(self.SMALLFONT, 'TOTAL', self.GREEN, self.BLACK)
		player_total_title.set_coords(75, 445)
		self.screen.blit(player_total_title.surface, player_total_title.rect)
		player_total_title = MyButton(self.BIGFONT, format(opponent['total']), self.GREEN, self.BLACK)
		player_total_title.set_coords(75, 485)
		self.screen.blit(player_total_title.surface, player_total_title.rect)
		# draw occupancy of the most occupied column
		player_longest_title = MyButton(self.SMALLFONT, 'LONGEST', self.YELLOW, self.BLACK)
		player_longest_title.set_coords(75, 525)
		self.screen.blit(player_longest_title.surface, player_longest_title.rect)
		player_longest_title = MyButton(self.BIGFONT, format(opponent['longest']), self.YELLOW, self.BLACK)
		player_longest_title.set_coords(75, 565)
		self.screen.blit(player_longest_title.surface, player_longest_title.rect)

	def animate_capture(self, ray_coords):
		if ray_coords['y'] >= ray_coords['top']:
			ray_coords['y'] = self.draw_ray(ray_coords)
			ray_coords['c'] += 1
			return True
		else:
			return False

	def animate_return(self, ray_coords):
		if ray_coords['y'] >= ray_coords['top']:
			ray_coords['y'] = self.draw_ray(ray_coords)
			ray_coords['c'] += 1
			return True
		else:
			return False

	def draw_explosion(self, targets, frame):
		image = None
		if frame < 6:
			image = self.fire1
		if frame < 11:
			image = self.fire2
		elif frame < 16:
			image = self.fire3

		for target in targets:
			position, height = target
			x = position * 90 + 175
			y = height * 50 + 50
			self.screen.blit(image, (x, y))

	def draw_ray(self, ray_coords):
		top = ray_coords['top']
		x = ray_coords['x']
		y = ray_coords['y']
		c = ray_coords['c']
		if y >= top:
			y = 500
			for i in range(c):
				y = y - 10 * c
				self.screen.blit(self.ray, (x, y))
		return y

	def draw_game_over(self):
		banner = MyButton(self.BIGFONT, '  GAME OVER  ', self.BLACK, self.YELLOW)
		banner.set_coords(W_WIDTH/2, W_HEIGHT/2)
		self.screen.blit(banner.surface, banner.rect)

	def draw_victory(self):
		banner = MyButton(self.BIGFONT, '  VICTORY!!!  ', self.BLACK, self.GREEN)
		banner.set_coords(W_WIDTH/2, W_HEIGHT/2)
		self.screen.blit(banner.surface, banner.rect)

	def confirm_exit(self):
		filter_rect = pygame.Rect((0, 0), (W_WIDTH, W_HEIGHT))
		pygame.draw.rect(self.screen, self.GREY, filter_rect)

		title = MyButton(self.MEDIUMFONT, 'CONFIRM EXIT', self.RED, self.BLACK)
		title.set_coords(W_WIDTH/2, 200)

		yes_button = MyButton(self.SMALLFONT, 'YES', self.BLACK, self.RED)
		yes_button.set_coords(W_WIDTH/2-100, 400)
		no_button = MyButton(self.SMALLFONT, 'NO', self.BLACK, self.GREEN)
		no_button.set_coords(W_WIDTH/2+100, 400)

		self.screen.fill(self.BLACK)
		self.screen.blit(yes_button.surface, yes_button.rect)
		self.screen.blit(no_button.surface, no_button.rect)
		self.screen.blit(title.surface, title.rect)

		return yes_button, no_button

	def confirm_leave_game(self):
		filter_rect = pygame.Rect((0, 0), (W_WIDTH, W_HEIGHT))
		pygame.draw.rect(self.screen, self.GREY, filter_rect)

		title = MyButton(self.MEDIUMFONT, 'CONFIRM LEAVE GAME', self.RED, self.BLACK)
		title.set_coords(W_WIDTH/2, 200)

		yes_button = MyButton(self.SMALLFONT, 'YES', self.BLACK, self.RED)
		yes_button.set_coords(W_WIDTH/2-100, 400)
		no_button = MyButton(self.SMALLFONT, 'NO', self.BLACK, self.GREEN)
		no_button.set_coords(W_WIDTH/2+100, 400)

		self.screen.fill(self.BLACK)
		self.screen.blit(title.surface, title.rect)
		self.screen.blit(yes_button.surface, yes_button.rect)
		self.screen.blit(no_button.surface, no_button.rect)

		return yes_button, no_button

	def update_game_screen(self, columns, player1):
		self.draw_game_board(player1)
		self.draw_figures(columns)
		self.draw_player(player1)


if __name__ == '__main__':
	pass
