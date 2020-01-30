import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import figure


class TestFigure(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestFigure, self).__init__(*args, **kwargs)

	def test_init(self):
		values = {'ball': 1, 'triangle': 2, 'square': 2, 'triangle-hole': 3, 'square-hole': 3}
		compatibility = {'ball': None, 'triangle': 'ball', 'square': 'ball', 'triangle-hole': 'triangle',
							'square-hole': 'square'}
		
		# SCENARIO 1: empty constructor
		# execute method
		test_figure = figure.Figure()
		# assert expected outcome
		# value of figure correctly initialized
		self.assertEqual(values[test_figure.shape], test_figure.value)
		
		# SCENARIO 2: loaded constructor
		# set state
		for figure_type, value in values.items():
			# execute method
			test_figure = figure.Figure(figure_type)
			# assert value of figure correctly initialized
			self.assertEqual(test_figure.value, value)
			
		# set state
		for key, value in compatibility.items():
			# execute method
			test_figure = figure.Figure(key)
			# assert compatibility value correctly initialized
			self.assertEqual(test_figure.compatible, value)

	def test_fits(self):
		compatibility = {'triangle': 'ball', 'square': 'ball', 'triangle-hole': 'triangle', 'square-hole': 'square'}
		
		for key, value in compatibility.items():
			# set state
			test_figure = figure.Figure(key)
			# execute method
			result = test_figure.fits(figure.Figure(value))
			# assert expected outcome
			self.assertTrue(result)
		
		# check ball is incompatible with all of them
		test_figure = figure.Figure('ball')
		for key, value in compatibility.items():
			# execute method
			result = test_figure.fits(figure.Figure(key))
			# assert expected outcome
			self.assertFalse(result)


if __name__ == '__main__':
	unittest.main()
