import string
import random


class Player:
	name = 'PLAYER 1'
	position = None
	captured_figure = None
	status = ''  # character's gameplay status: empty | full | | capturing | returning
	online = ''  # Player's online status: '' | connected | available | ready | playing
	score = 0
	steps = 0		# player step counter for row generation
	ID = ''		# random string to id player, requires reboot to change

	def __init__(self):
		# set center position
		self.position = 3 
		# set emtpy status
		self.status = 'empty'
		# create and assign random player ID
		all_chars = string.ascii_letters + string.digits  # + string.punctuation
		self.ID = ''.join(random.choice(all_chars) for x in range(10))
		print(f'[Player] Initialized {self.ID}')

	def move_player(self, direction):
		if direction is 'left' and self.position > 0:
			self.position -= 1
			self.steps += 1
		elif direction is 'right' and self.position < 6:
			self.position += 1
			self.steps += 1

	def capture_figure(self, figure):
		self.captured_figure = figure
		self.status = 'full'
		print('[player] Capture: {}'.format(figure.shape))

	def action(self, columns):
		# capture the player's position (0-6)
		player_position = self.position
		# check how many figures in column
		active_column_occupancy = columns[player_position].occupancy()
		# dictionary of coordinates for the ray to be drawn
		ray_coords = {
			'position': 0,		# player's position in the board (column number)
			'top': 0,			# where the first figure in that column starts, in pixels
			'x': 0,				# pixel number of x coordinate for ray start
			'y': 0,				# pixel number of x coordinate for ray start
			'c': 0				# counter
		}

		if self.status == 'empty' and active_column_occupancy > 0:
			self.status = 'capturing'
			# print('[player] {} @ column #{}'.format(self.player.status, position))
			x = player_position * 90 + 180
			y = 500
			top = 500 - active_column_occupancy * 50
			c = 1
			ray_coords = {'position': player_position, 'top': top, 'x': x, 'y': y, 'c': c}
		elif self.status == 'full' and active_column_occupancy < 10:
			self.status = 'returning'
			# print('[player] {} @ column #{}'.format(self.player.status, position))
			x = player_position * 90 + 180
			y = 475
			top = 500 - active_column_occupancy * 50
			c = 1
			ray_coords = {'position': player_position, 'top': top, 'x': x, 'y': y, 'c': c}
		elif self.status in ('capturing', 'returning'):
			# this probably never happens
			print("[player] Patience, small grasshopper")

		# print('[#] {} @ column #{}'.format(self.status, position+1))
		return ray_coords

	def empty(self):
		self.captured_figure = None
		self.status = 'empty'

	def reset(self):
		self.captured_figure = None
		self.status = 'empty'
		self.online = ''
		self.score = 0
		self.steps = 0

	def get_stats(self):
		stats = {
			'id': self.ID,				# player's id string
			'name': self.name,			# name chosen by player
			'status': self.status,		# status of the game's character
			'score': self.score,		# current game score
		}
		return stats


if __name__ == '__main__':
	pass
