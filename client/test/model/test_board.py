import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import board


class TestBoard(unittest.TestCase):
	
	my_board = None

	def __init__(self, *args, **kwargs):
		super(TestBoard, self).__init__(*args, **kwargs)

	def test_create_columns(self):
		# set object state
		# execute method
		test_board = board.Board()
		# assert expected outcome
		self.assertEqual(len(test_board.columns), 7)

	def test_add_row(self):
		# count all figures in board
		before = 0
		test_board = board.Board()
		for column in test_board.columns:
			before += column.occupancy()
		
		# execute method
		test_board.add_row()
		
		# assert expected outcome
		# count all figures in board
		after = 0
		for column in test_board.columns:
			after += column.occupancy()
		# 1 row == 7 figures
		self.assertEqual(after, before + 7)
	
	def test_update_counts(self):
		# set object state
		test_board = board.Board()
		my_figure_count = 0
		my_longest = 0
		for column in test_board.columns:
			my_figure_count += column.occupancy()
			if column.occupancy() > my_longest:
				my_longest = column.occupancy()
		# execute method
		test_board.update_counts()
		# assert expected outcome
		self.assertEqual(my_figure_count, test_board.figure_count)
		self.assertEqual(my_longest, test_board.longest_column_count)
	
	# def test_acquire_targets(self):
	# 	# clears target list and executes acquire_targets()
	# 	# set object state
	#
	# 	# execute method
	#
	# 	# assert expected outcome
	# 	pass
	#
	# def test_acquire_targets(self):
	# 	# fill the columns with controlled figures for known results
	# 	pass
	#
	# def test_eliminate_targets(self):
	# 	# use fabricated column content to asses expected points resulted from the elimination
	# 	pass


if __name__ == '__main__':
	unittest.main()
