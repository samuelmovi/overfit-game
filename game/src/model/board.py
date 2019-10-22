from model import column
from model import figure


class Board:
	columns = []
	targets = []
	explosion_counter = 1
	longest_column_count = 0

	def __init__(self):
		self.create_columns()
		pass

	def create_columns(self):
		# reset and populate columns
		self.columns.clear()
		for n in range(7):
			my_column = column.Column()
			self.columns.append(my_column)

	def add_row(self):
		for i in range(7):
			self.columns[i].figures.insert(0, figure.Figure())
	
	def check_longest_column(self):
		total = 0
		longest = 0
		for c in self.columns:
			length = c.occupancy()
			total += length
			if length > longest:
				longest = length
		self.longest_column_count = longest
	
	def all_targets(self, position, height):
		self.targets.clear()
		return self.acquire_targets(position, height)

	def acquire_targets(self, position, height):
		compatible = [(position, height)]
		target_shape = self.columns[position].figures[height].shape

		if (height+1) < self.columns[position].occupancy():
			if self.columns[position].figures[height+1].shape == target_shape:
				if (position, height+1) not in self.targets:
					compatible.append((position, height+1))
		# explode on the left
		if position > 0 and self.columns[position-1].occupancy() >= (height + 1):
			if self.columns[position - 1].figures[height].shape == target_shape:
				if (position-1, height) not in self.targets:
					compatible.append((position-1, height))
		# explode on the right
		if position < 6 and height < self.columns[position+1].occupancy():
			if self.columns[position + 1].figures[height].shape == target_shape:
				if (position+1, height) not in self.targets:
					compatible.append((position+1, height))
		# explode on top
		if height > 0:
			if self.columns[position].figures[height-1].shape == target_shape:
				if (position, height-1) not in self.targets:
					compatible.append((position, height-1))
		# check the list and add if missing
		for target in compatible:
			if target not in self.targets:
				self.targets.append(target)
				self.acquire_targets(target[0], target[1])

		return self.targets

	def eliminate_targets(self, target_list):
		score = 0
		for coordinates in target_list:
			position, height = coordinates
			print('[*] Destroying target #{} @ {} / {}  :   {} points'.format(
				self.explosion_counter,
				position,
				height,
				self.columns[position].figures[height].value))
			# update score
			score += self.columns[position].figures[height].value
			self.columns[position].figures.pop(height)
			self.explosion_counter += 1
		self.targets.clear()
		return score


if __name__ == '__main__':
	pass