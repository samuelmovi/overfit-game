import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import column


class TestColumn(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestColumn, self).__init__(*args, **kwargs)
		
	def test_init(self):
		# execute method
		test_column = column.Column()
		# assert expected outcome
		self.assertIsNotNone(test_column.figures)
		self.assertTrue(len(test_column.figures) >= 2)
		self.assertTrue(len(test_column.figures) <= 5)

	def test_occupancy(self):
		# execute method
		test_column = column.Column()
		test_column.figures = [1]
		# assert expected outcome
		self.assertEqual(test_column.occupancy(), 1)


if __name__ == '__main__':
	unittest.main()
