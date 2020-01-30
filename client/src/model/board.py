from model import column
from model import figure


class Board:
	columns = []		# list of column objects
	# targets = []		# list of tuples of target coordinates (position, height)
	# explosion_counter = 1
	longest_column_count = 0
	figure_count = 0
	
	def setup(self):
		# create the columns, with its figures
		self.create_columns()
		# update values to the newly created columns
		self.update_counts()
	
	def create_columns(self):
		# reset and populate columns
		self.columns.clear()
		for n in range(7):
			new_column = column.Column()
			self.columns.append(new_column)

	def add_row(self):
		for i in range(7):
			self.columns[i].figures.insert(0, figure.Figure())
	
	def update_counts(self):
		total_count = 0
		longest = 0
		for c in self.columns:
			length = c.occupancy()
			total_count += length
			if length > longest:
				longest = length
		self.figure_count = total_count
		self.longest_column_count = longest

	def acquire_targets(self, column_index, height):
		targets = []
		compatible = [(column_index, height)]
		# get shape of figure @ coordinates
		target_shape = self.columns[column_index].figures[height].shape
		# add compatible adjacent figures to self.targets
		if (height+1) < self.columns[column_index].occupancy():
			if self.columns[column_index].figures[height + 1].shape == target_shape:
				if (column_index, height + 1) not in targets:
					compatible.append((column_index, height + 1))
		# on the left
		if column_index > 0 and self.columns[column_index - 1].occupancy() >= (height + 1):
			if self.columns[column_index - 1].figures[height].shape == target_shape:
				if (column_index - 1, height) not in targets:
					compatible.append((column_index - 1, height))
		# on the right
		if column_index < 6 and height < self.columns[column_index + 1].occupancy():
			if self.columns[column_index + 1].figures[height].shape == target_shape:
				if (column_index + 1, height) not in targets:
					compatible.append((column_index + 1, height))
		# on top
		if height > 0:
			if self.columns[column_index].figures[height - 1].shape == target_shape:
				if (column_index, height - 1) not in targets:
					compatible.append((column_index, height - 1))
		# check the list and add if missing, to avoid errors
		for target in compatible:
			if target not in targets:
				targets.append(target)
				self.acquire_targets(target[0], target[1])
		return targets

	def eliminate_targets(self, target_list):
		score = 0
		for coordinates in target_list:
			position, height = coordinates
			print(f'[*] Destroying target [{position} / {height}]:  {self.columns[position].figures[height].value} points')
			# update score
			score += self.columns[position].figures[height].value
			self.columns[position].figures.pop(height)
			# self.explosion_counter += 1
		# self.targets.clear()
		return score


if __name__ == '__main__':
	pass
