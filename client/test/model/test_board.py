import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import board
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
	# 	# set object state
	#	test_board = board.Board()
	#	test_board.setup()
	#	# SCENARIOS: specific column loads for expected outcome
	#	test_position = 1	# between 0-6
	#	test_height = 5
	# 	# execute method
	#	test_board.acquire_targers(test_position, test_height)
	# 	# assert expected outcome
	# 	pass
	
	def test_eliminate_targets(self):
		# set state
		test_board = board.Board()
		test_board.setup()
		
		# create test targets
		test_targets = [(0, 5)]
		# execute method
		test_score = test_board.eliminate_targets(test_targets)
		# assert expected outcome
		self.assertIsNotNone(test_score)


if __name__ == '__main__':
	unittest.main()
