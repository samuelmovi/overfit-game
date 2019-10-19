import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import column


class TestColumn(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestColumn, self).__init__(*args, **kwargs)
		pass

	def test_occupancy(self):
		print("[#] Testing method: Column.occupancy()")
		my_column = column.Column()
		self.assertEqual(my_column.occupancy(), len(my_column.figures))


if __name__ == '__main__':
	unittest.main()
