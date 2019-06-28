import random


class Figure:

	empty = True
	value = 0
	shape = ''  # shapes: square, triangle, ball, square-hole, triangle-hole
	compatible = ''
	FIGURE_SHAPES = ['ball', 'triangle', 'square', 'triangle-hole', 'square-hole']

	def __init__(self, this_shape=None):
		if this_shape is None:
			self.shape = self.FIGURE_SHAPES[random.randint(0, len(self.FIGURE_SHAPES)-1)]
		else:
			self.shape = this_shape

		if self.shape == 'triangle':
			self.compatible = 'ball'
			self.value = 2
		elif self.shape == 'square':
			self.compatible = 'ball'
			self.value = 2
		elif self.shape == 'triangle-hole':
			self.compatible = 'triangle'
			self.value = 3
		elif self.shape == 'square-hole':
			self.compatible = 'square'
			self.value = 3
		else:  # if it's a ball
			self.compatible = None
			self.value = 1

	def fits(self, figure):
		if figure.shape == self.compatible:
			return True
		else:
			return False


if __name__ == '__main__':
	pass
