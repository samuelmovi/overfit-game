import unittest
from unittest.mock import Mock
import sys
import os
# sys.path.append(os.path.abspath(sys.path[0]) + '/../../game/')
sys.path.append(os.path.abspath('../../game/'))
from model import board


class FigurePatch:
	pass


class ColumnPatch:
	pass


class TestBoard(unittest.TestCase):
	
	my_board = None

	def __init__(self, *args, **kwargs):
		super(TestBoard, self).__init__(*args, **kwargs)
		pass

	def test_create_columns(self):
		print("[#] Testing method: Board.create_columns()")
		self.my_board = board.Board()
		self.assertEqual(len(self.my_board.columns), 7)

	def test_add_row(self):
		print("[#] Testing method: Board.add_row()")
		# since a row is 7 figures the total count of the columns contents must be +7
		first_total = 0
		self.my_board = board.Board()
		for column in self.my_board.columns:
			first_total += column.occupancy()

		self.my_board.add_row()

		second_total = 0
		for column in self.my_board.columns:
			second_total += column.occupancy()

		self.assertEqual(second_total, first_total+7)

	def test_all_targets(self):
		# clears target list and executes acquire_targets()
		pass

	def test_acquire_targets(self):
		# fill the columns with controlled figures for known results
		pass

	def test_eliminate_targets(self):
		# use fabricated column content to asses expected points resulted from the elimination
		pass


if __name__ == '__main__':
	unittest.main()
