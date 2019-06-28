import random
from model import figure


class Column:
	figures = None

	def __init__(self):
		self.figures = list()
		for n in range(random.randint(2, 5)):
			self.figures.append(figure.Figure())
		print('[#] Column created: {} Figures'.format(self.occupancy()))

	def occupancy(self):
		return len(self.figures)


if __name__ == '__main__':
	pass
