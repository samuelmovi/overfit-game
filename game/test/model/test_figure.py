import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import figure


class TestFigure(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestFigure, self).__init__(*args, **kwargs)
		my_figure = figure.Figure()
		pass

	def test_init(self):
		print("[#] Testing method: Figure.__init__(shape)")
		values = {'ball': 1, 'triangle': 2, 'square': 2, 'triangle-hole': 3, 'square-hole': 3}
		for key, value in values.items():
			my_figure = figure.Figure(key)
			self.assertEqual(my_figure.value, value)

	def test_fits(self):
		print("[#] Testing method: Figure.fits(figure)")
		compatibility = {'ball': None, 'triangle': 'ball', 'square': 'ball', 'triangle-hole': 'triangle', 'square-hole': 'square'}
		for key, value in compatibility.items():
			my_figure = figure.Figure(key)
			self.assertEqual(my_figure.compatible, value)


if __name__ == '__main__':
	unittest.main()
