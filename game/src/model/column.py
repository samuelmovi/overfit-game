import random
from model import figure

# creates a column with a random number of figures, between 2 and 5


class Column:

	def __init__(self):
		self.figures = list()
		for n in range(random.randint(2, 5)):
			self.figures.append(figure.Figure())
		print('[#] New column: {} Figures'.format(self.occupancy()))

	def occupancy(self):
		return len(self.figures)


if __name__ == '__main__':
	pass
