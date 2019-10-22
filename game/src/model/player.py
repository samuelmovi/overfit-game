import string
import random


class Player:
	name = 'PLAYER 1'
	position = None
	captured_figure = None
	status = ''  # empty | full | | capturing | returning
	online = ''  # '' | available | challenger | accepted | itson | playing | over
	score = 0
	steps = 0
	connected = False
	ID = ''

	def __init__(self):
		self.position = 3  # starts in middle of 7 columns
		self.status = 'empty'
		all_chars = string.ascii_letters + string.digits  # + string.punctuation
		self.ID = ''.join(random.choice(all_chars) for x in range(10))

	def move_player(self, direction):
		if direction is 'left' and self.position > 0:
			self.position -= 1
		elif direction is 'right' and self.position < 6:
			self.position += 1
		self.steps += 1

	def capture_figure(self, figure):
		self.captured_figure = figure
		self.status = 'full'
		print('[player] Capture: {}'.format(figure.shape))

	def action(self, columns):
		# store player position in case it changes
		position = self.position
		active_column_occupancy = columns[position].occupancy()
		ray_coords = {'position': 0, 'top': 0, 'x': 0, 'y': 0, 'c': 0}

		if self.status == 'empty' and active_column_occupancy > 0:
			self.status = 'capturing'
			# print('[player] {} @ column #{}'.format(self.player.status, position))
			x = position * 90 + 180
			y = 500
			top = 500 - active_column_occupancy * 50
			c = 1
			ray_coords = {'position': position, 'top': top, 'x': x, 'y': y, 'c': c}

		elif self.status == 'full' and active_column_occupancy < 10:
			self.status = 'returning'
			# print('[player] {} @ column #{}'.format(self.player.status, position))
			x = position * 90 + 180
			y = 475
			top = 500 - active_column_occupancy * 50
			c = 1
			ray_coords = {'position': position, 'top': top, 'x': x, 'y': y, 'c': c}
		else:
			print("[player] WEIRD FUCKING THING HAPPENNED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			print("[player] Either: player and column empty, or player and column full")

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
		self.connected = False

	def get_stats(self):
		stats = {
			'sender': self.ID,			# random string that identifies player in server
			'name': self.name,			# name chosen by player
			'online': self.online,		# player's online status
			'status': self.status,		# status of the game's character
			'score': self.score}		# current game score
		return stats


if __name__ == '__main__':
	pass
