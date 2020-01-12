import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import figure


class TestFigure(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestFigure, self).__init__(*args, **kwargs)

	def test_init(self):
		# set object value
		values = {'ball': 1, 'triangle': 2, 'square': 2, 'triangle-hole': 3, 'square-hole': 3}
		compatibility = {'ball': None, 'triangle': 'ball', 'square': 'ball', 'triangle-hole': 'triangle',
							'square-hole': 'square'}
		
		# execute method: empty constructor
		test_figure = figure.Figure()
		# value of figure correctly initialized
		self.assertEqual(values[test_figure.shape], test_figure.value)
		
		# execute method: loaded constructor
		for key, value in values.items():
			test_figure = figure.Figure(key)
			# value of figure correctly initialized
			self.assertEqual(test_figure.value, value)
			
		# execute method
		for key, value in compatibility.items():
			test_figure = figure.Figure(key)
			# compatibility value correclty initialized
			self.assertEqual(test_figure.compatible, value)

	def test_fits(self):
		# set context
		compatibility = {'triangle': 'ball', 'square': 'ball', 'triangle-hole': 'triangle', 'square-hole': 'square'}
		
		# execute method
		for key, value in compatibility.items():
			test_figure = figure.Figure(key)
			# assert expected outcome
			self.assertEqual(test_figure.fits(figure.Figure(value)), True)
		
		# execute method
		test_figure = figure.Figure('ball')
		for key, value in compatibility.items():
			# assert expected outcome
			self.assertEqual(test_figure.fits(figure.Figure(value)), False)


if __name__ == '__main__':
	unittest.main()
