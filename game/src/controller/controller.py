import pygame
import sys
import time
import json
import os
from pygame.locals import *
from model import board, zmq_connector, online_broker


class Controller:
	RIGHT = 'right'
	LEFT = 'left'
	FPS = 30  # frames per second to update the screen
	AP_Q = 'ap_q'
	opponent = None  # used to store the opponents dictionaries
	send_counter = 0  # used to delay checking queues
	explosion_counter = 1
	rows_received = 1
	ray_coords = {}
	frame = 0  # to keep track of frames during explosion animations
	all_targets_acquired = False
	player_stats = {}  # dictionary for the players own stats
	board = None
	broker = None
	mq = None
	HOST = '127.0.0.1'
	
	my_view = None
	player = None
	targets = []
	FPSCLOCK = None
	base_dir = os.getcwd()

	def __init__(self, view, player):
		print('[#] Initiating Controller...')
		pygame.init()
		pygame.mixer.quit()
		
		self.my_view = view
		self.my_view.set_up_fonts()
		self.load_external_resources(self.my_view)

		self.player = player

		self.FPSCLOCK = pygame.time.Clock()
		pygame.display.set_caption('WeeriMeeris')
		
		self.start_screen()
	
	@staticmethod
	def load_external_resources(my_view, base_dir):
		
		my_view.ball = pygame.image.load(os.path.join(base_dir, 'resources/ball.png'))
		my_view.triangle_full = pygame.image.load(os.path.join(base_dir, 'resources/triangle-pink-full.png'))
		my_view.triangle_empty = pygame.image.load(
			os.path.join(base_dir, 'resources/triangle-pink-empty.png'))
		my_view.square_full = pygame.image.load(os.path.join(base_dir, 'resources/square-yellow-full.png'))
		my_view.square_empty = pygame.image.load(os.path.join(base_dir, 'resources/square-yellow-empty.png'))
		my_view.triangle_hole_complete = pygame.image.load(
			os.path.join(base_dir, 'resources/triangle-hole-green-complete.png'))
		my_view.triangle_hole_full = pygame.image.load(
			os.path.join(base_dir, 'resources/triangle-hole-green-full.png'))
		my_view.triangle_hole_empty = pygame.image.load(
			os.path.join(base_dir, 'resources/triangle-hole-green-empty.png'))
		my_view.square_hole_complete = pygame.image.load(
			os.path.join(base_dir, 'resources/square-hole-red-complete.png'))
		my_view.square_hole_full = pygame.image.load(
			os.path.join(base_dir, 'resources/square-hole-red-full.png'))
		my_view.square_hole_empty = pygame.image.load(
			os.path.join(base_dir, 'resources/square-hole-red-empty.png'))
		my_view.player_full = pygame.image.load(os.path.join(base_dir, 'resources/player-full.png'))
		my_view.player_empty = pygame.image.load(os.path.join(base_dir, 'resources/player-empty.png'))
		
		my_view.fire1 = pygame.image.load(os.path.join(base_dir, 'resources/fire1.png'))
		my_view.fire2 = pygame.image.load(os.path.join(base_dir, 'resources/fire2.png'))
		my_view.fire3 = pygame.image.load(os.path.join(base_dir, 'resources/fire3.png'))
		
		my_view.ray = pygame.image.load(os.path.join(base_dir,'resources/ray-short.png'))

	# SCREENS
	def start_screen(self):
		single_player_button, online_multi_button, settings_button = self.my_view.draw_start_screen()

		while True:
			for event in pygame.event.get():  # event handling loop
				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.confirm_exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_x, mouse_y = event.pos
					if single_player_button.rect.collidepoint((mouse_x, mouse_y)):
						self.play()
					elif online_multi_button.rect.collidepoint((mouse_x, mouse_y)):
						self.online_setup_screen()
					elif settings_button.rect.collidepoint((mouse_x, mouse_y)):
						self.settings_screen()
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def online_setup_screen(self):
		print('[#] Showing Online Setup screen')
		inputs, start_button = self.my_view.draw_online_options_screen(self.player.name, self.HOST)
		while True:
			# event handling loop
			for event in pygame.event.get():
				# handle events in inputs first
				for input_box in inputs:
					input_box.handle_event(event)

				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.event.clear()
						self.start_screen()
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_x, mouse_y = event.pos
					if start_button.rect.collidepoint((mouse_x, mouse_y)):
						if len(inputs[0].get_text()) > 0:
							self.HOST = inputs[0].get_text()
						if len(inputs[1].get_text()) > 0:
							self.player.name = inputs[1].get_text()
						self.find_online_match()
			self.my_view.refresh_input(inputs)
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def settings_screen(self):
		print('[#] Showing settings screen')
		inputs, save_button = self.my_view.draw_settings_screen(self.player.name, self.HOST)
		while True:
			# event handling loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.event.clear()
						self.start_screen()
					elif event.key == pygame.K_RETURN:
						if len(inputs[0].get_text()) > 0:
							self.mq.HOST = inputs[0].get_text()
						if len(inputs[1].get_text()) > 0:
							self.player.name = inputs[1].get_text()
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_x, mouse_y = event.pos
					if save_button.rect.collidepoint((mouse_x, mouse_y)):
						self.HOST = inputs[0].text
						self.player.name = inputs[1].text
						print("[#] Data updated\n\t> Host: {}\n\t> Player Name: {}".format(inputs[0].text, inputs[1].text))
				for instance in inputs:
					instance.handle_event(event)
			self.my_view.refresh_input(inputs)
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def confirm_exit(self):
		yes_button, no_button = self.my_view.confirm_exit()
		while True:
			for event in pygame.event.get():  # event handling loop
				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.start_screen()
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_x, mouse_y = event.pos
					if yes_button.rect.collidepoint((mouse_x, mouse_y)):
						self.shutdown()
					elif no_button.rect.collidepoint((mouse_x, mouse_y)):
						self.start_screen()
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def confirm_leave_game(self):
		yes_button, no_button = self.my_view.confirm_leave_game()
		while True:
			for event in pygame.event.get():  # event handling loop
				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.MOUSEBUTTONUP:
					mouse_x, mouse_y = event.pos
					if yes_button.rect.collidepoint((mouse_x, mouse_y)):
						self.reset_state()
						self.start_screen()
					elif no_button.rect.collidepoint((mouse_x, mouse_y)):
						return
				"""
				# THIS CODE CRASHES GAME FOR UNKNOWN REASON
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.event.clear()
					return
				"""
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	# GAMING FUNCTIONS
	def play(self):
		print('[#] Game START!')
		self.board = board.Board()
		print('[#] Opponent: {}'.format(self.opponent))

		while True:
			self.check_player_events()
			self.update_player_stats()
			self.my_view.update_game_screen(self.board.columns, self.player)
			self.check_online_play()

			# check for capture
			if self.player.status == 'capturing':
				self.capture_animation()
			# check for return
			elif self.player.status == 'returning':
				self.return_animation()
			# check for explosion
			if self.all_targets_acquired is True:
				self.explode_all_targets()

			# Refresh screen and wait a clock tick.
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def capture_animation(self):
		if self.my_view.animate_return(self.ray_coords) is False:
			# remove bottom figure from column and capture it
			self.player.capture_figure(self.board.columns[self.ray_coords['position']].figures.pop(-1))

	def return_animation(self):
		if self.my_view.animate_return(self.ray_coords) is False:
			# after the ray has finished being drawn
			# if column is empty add captured figure to column
			if len(self.board.columns[self.ray_coords['position']].figures) == 0:
				self.board.columns[self.ray_coords['position']].figures.append(self.player.captured_figure)
			# if bottom figure in column fits captured figure
			elif self.board.columns[self.ray_coords['position']].figures[-1].fits(self.player.captured_figure):
				# and  bottom figure is empty, fit them
				if self.board.columns[self.ray_coords['position']].figures[-1].empty is True:
					self.board.columns[self.ray_coords['position']].figures[-1].value += self.player.captured_figure.value
					self.board.columns[self.ray_coords['position']].figures[-1].empty = False
				else:
					# if bottom figure is not empty
					# list adjacent compatible figures
					self.targets = self.board.all_targets(self.player.position, self.board.columns[self.player.position].occupancy() - 1)
					self.all_targets_acquired = True
					self.player.score += self.player.captured_figure.value
					print('[#] All targets acquired: {} [{}]'.format(self.all_targets_acquired, len(self.targets)))
					for target in self.targets:
						print('\t> Position: {}\t> Height: {}'.format(target[0], target[1]))
					self.frame = 0
			else:
				# if figures don't fit add to column
				self.board.columns[self.ray_coords['position']].figures.append(self.player.captured_figure)
			self.player.empty()

	def explode_all_targets(self):
		if self.frame < 16:
			self.my_view.draw_explosion(self.targets, self.frame)
			self.frame += 1
		else:
			# sorting targets by height, to avoid IndexOutOfBoundsError
			self.targets.sort(key=lambda x: x[1], reverse=True)
			self.player.score += self.board.eliminate_targets(self.targets)
			self.frame = 0

	def check_player_events(self):
		# event handling loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
				self.shutdown()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.player.move_player(self.LEFT)
				elif event.key == pygame.K_RIGHT:
					self.player.move_player(self.RIGHT)
				elif event.key == pygame.K_SPACE:
					self.ray_coords = self.player.action(self.board.columns)
				elif event.key == pygame.K_ESCAPE:
					pygame.event.clear()
					self.confirm_leave_game()

	def update_player_stats(self):
		# check to add new row to self
		if self.player.steps > 15 or self.player.total < 15:
			self.board.add_row()
			self.player.steps = 0
		# recounting stuff
		total = 0
		longest = 0
		for c in self.board.columns:
			length = c.occupancy()
			total += length
			if length > longest:
				longest = length
		self.player.total = total
		self.player.longest = longest
		# check endgame condition
		if self.player.longest >= 10:
			self.game_over()

	# ONLINE FUNCTIONS
	def find_online_match(self):
		print('[#] Finding online match...')
		self.mq = zmq_connector.ZmqConnector(self.HOST)
		self.broker = online_broker.OnlineBroker(self.player, self.mq)

		text = ''
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
					self.shutdown()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.event.clear()
						self.broker = None
						self.reset_state()
						self.start_screen()

			opponent = self.broker.negotiate()
			if opponent is not None:
				self.player.online = 'playing'
				self.opponent = opponent
				self.play()

			# set text for wait-screen
			if self.player.online == 'available':
				text = 'Waiting for challengers'
				# self.broker.timer += 1
			elif self.player.online == 'accepted':
				text = 'Challenge has been accepted'
				# self.broker.timer += 1
			elif self.player.online == 'challenger':
				text = 'Challenging available opponent'
				# self.broker.timer += 1
			elif self.player.online == 'itson':
				# self.broker.timer += 1
				text = 'It\'s F**king ON!!!'
				# self.player.online = 'playing'

			if self.broker.timeout() is True:
				break

			self.my_view.draw_wait_screen(text)
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def check_online_play(self):
		if self.player.connected is True:
			# send  message every 10 frames, read every 20
			if self.send_counter > 10:
				self.send_counter = 0
				self.check_on_opponent()
				self.broker.update_player_stats()
			self.send_counter += 1
			# draw opponents score board
			self.my_view.draw_opponent(self.opponent)

	def check_on_opponent(self):
		message = self.mq.sub_receive_multi()
		if message is not None:
			print("[#] Opponent update: {}".format(message))
			self.opponent = json.loads(message[1].decode())
		if self.opponent['online'] == 'over':
			self.victory()
		elif self.opponent['online'] == 'playing':
			if self.rows_received * 20 < int(self.opponent['score']):
				print('[#] Received row')
				self.board.add_row()
				self.rows_received += 1

	# END GAME
	def game_over(self):
		self.my_view.draw_game_over()

		while True:
			# event handling loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.event.clear()
					self.reset_state()
					self.start_screen()
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def victory(self):
		self.my_view.draw_victory()

		while True:
			# event handling loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.shutdown()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pygame.event.clear()
					self.reset_state()
					self.start_screen()
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def reset_state(self):
		if self.mq is not None:
			self.player.online = 'over'
			print('[player] {}'.format(self.player.online))
			if self.opponent is not None:
				message = [self.opponent['sender'], json.dumps(self.player.get_stats())]
				for i in range(len(message)):
					message[i] = message[i].encode()
				self.mq.push_send_multi(message)
			time.sleep(1)
			self.mq.disconnect()

		self.opponent = None
		self.send_counter = 0
		self.explosion_counter = 1
		self.rows_received = 0
		self.player.reset()

	def shutdown(self):
		pygame.quit()
		sys.exit()


if __name__ == '__main__':
	pass
