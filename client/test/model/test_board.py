import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import board, figure, column
from unittest import mock


class TestBoard(unittest.TestCase):
	
	def __init__(self, *args, **kwargs):
		super(TestBoard, self).__init__(*args, **kwargs)

	def test_setup(self):
		# set state
		test_board = board.Board()
		test_board.create_columns = mock.Mock()
		test_board.update_counts = mock.Mock()
		# execute method
		test_board.setup()
		# assert expected outcome
		self.assertTrue(test_board.create_columns.called)
		self.assertTrue(test_board.update_counts.called)
	
	def test_create_columns(self):
		# set object state
		test_board = board.Board()
		# execute method
		test_board.create_columns()
		# assert expected outcome
		self.assertEqual(len(test_board.columns), 7)

	def test_add_row(self):
		# count all figures in board
		test_board = board.Board()
		test_board.setup()
		# get count on figures in columns
		before = 0
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
		test_board.setup()
		# pre-execution counters
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
	# 	# TODO: fix recursion error
	# 	# set object state
	# 	test_board = board.Board()
	# 	test_board.setup()
	# 	# clear board's columns
	# 	for c in test_board.columns:
	# 		c.figures = []
	#
	# 	# SCENARIOS: all figures the same
	# 	for i in range(5):
	# 		test_board.columns[i].figures.append(figure.Figure('square'))
	# 	# execute method, on first column top height
	# 	result = test_board.acquire_targets(0, 0)
	# 	# assert expected outcome
	# 	self.assertIsNotNone(result)
	# 	self.assertEqual(len(result), 5)
	
	def test_eliminate_targets(self):
		# TODO: create extra testing scenarios
		# set state
		test_board = board.Board()
		test_board.setup()
		for c in test_board.columns:
			c.figures = []
		
		for i in range(3):
			test_board.columns[0].figures.append(figure.Figure('square'))
	
		test_targets = [(0, 2), (0, 1), (0, 0)]
		# execute method
		result = test_board.eliminate_targets(test_targets)
		# assert expected outcome
		self.assertIsNotNone(result)
		self.assertEqual(len(test_board.columns[0].figures), 0)
		self.assertEqual(result, 6)		# 3 squares, each 2 points


if __name__ == '__main__':
	unittest.main()
