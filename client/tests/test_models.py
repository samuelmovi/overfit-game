import unittest
import sys
import os
sys.path.append(os.path.abspath('../src/'))
from model import board, figure, column, player, online_broker, zmq_client
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


class TestOnlineBroker(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestOnlineBroker, self).__init__(*args, **kwargs)
		pass
	
	def test_init(self):
		# set state
		mock_mq = mock.Mock()
		mock_player = mock.Mock()
		# execute method
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		# check initial state
		self.assertIsNotNone(test_broker.player)
		self.assertIsNotNone(test_broker.mq)
		self.assertEqual(mock_player, test_broker.player)
		self.assertEqual(mock_mq, test_broker.mq)

	def test_set_player_available(self):
		# set state
		mock_mq = mock.Mock()
		mock_player = mock.Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		# execute method
		test_broker.set_player_available()
		# assert expected changes
		self.assertEqual(mock_player.online, 'available')
		self.assertTrue(mock_mq.send.called)

	def test_check_for_ready(self):
		# set state
		mock_mq = mock.Mock()
		mock_player = mock.Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		mock_mq.sub_receive_multi.return_value = [0, b'{"sender": "SERVER", "status": "READY"}', 1]
		# execute method
		test_broker.check_for_ready()
		# assert expected results
		self.assertEqual(mock_player.online, 'ready')
		self.assertTrue(mock_mq.send.called)
	
	def test_check_for_start(self):
		# set state
		mock_mq = mock.Mock()
		mock_player = mock.Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		# SCENARIO 1: no start
		mock_mq.sub_receive_multi.return_value = [0, b'{"sender": "SERVER", "status": "qwerwqe"}', 1]
		# execute method
		result = test_broker.check_for_start()
		# assert expected results
		self.assertIsNone(result)
		
		# SCENARIO 2: start
		mock_mq.sub_receive_multi.return_value = [0, b'{"sender": "OPPONENT_ID", "status": "START"}', 1]
		# execute method
		result = test_broker.check_for_start()
		# assert expected results
		self.assertIsNotNone(result)
		self.assertEqual(result, "OPPONENT_ID")
	
	def test_negotiate_match(self):
		# set state
		mock_mq = mock.Mock()
		mock_player = mock.Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		# SCENARIOS for player.online: connected, available, ready
		# connected
		test_broker.set_player_available = mock.Mock()
		mock_player.online = 'connected'
		# execute method
		response = test_broker.negotiate_match()
		# assert expected outcome
		self.assertIsNone(response)
		self.assertTrue(test_broker.set_player_available.called)
		
		# available
		test_broker.check_for_ready = mock.Mock()
		mock_player.online = 'available'
		# execute method
		response = test_broker.negotiate_match()
		# assert expected outcome
		self.assertIsNone(response)
		self.assertTrue(test_broker.check_for_ready.called)
		
		# ready
		test_broker.check_for_start = mock.Mock()
		test_broker.check_for_start.return_value = 1
		mock_player.online = 'ready'
		# execute method
		response = test_broker.negotiate_match()
		# assert expected outcome
		self.assertIsNotNone(response)
		self.assertTrue(test_broker.check_for_start.called)

	def test_quit(self):
		# set state
		mock_mq = mock.Mock()
		mock_player = mock.Mock()
		test_broker = online_broker.OnlineBroker(mock_player, mock_mq)
		
		# execute method
		test_broker.quit()
		
		# assert expected outcome
		self.assertTrue(mock_mq.send.called)
		self.assertTrue(mock_mq.disconnect.called)


class TestPlayer(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPlayer, self).__init__(*args, **kwargs)
    
    def test_init(self):
        # execute method
        test_player = player.Player()
        # assert expected outcome
        self.assertEqual('empty', test_player.status)
        self.assertEqual(10, len(test_player.ID))
        self.assertEqual(3, test_player.position)
    
    def test_move_player(self):
        # set object state
        test_player = player.Player()
        test_position = 5
        steps_before = test_player.steps
        LEFT = 'left'
        RIGHT = 'right'
        
        # execute method
        test_player.position = test_position
        test_player.move_player(LEFT)
        # assert expected outcome
        self.assertEqual(test_position - 1, test_player.position)
        self.assertEqual(steps_before + 1, test_player.steps)

        # set object state
        steps_before = test_player.steps
        test_player.position = test_position
        # execute method
        test_player.move_player(RIGHT)
        # assert expected outcome
        self.assertEqual(test_position + 1, test_player.position)
        self.assertEqual(steps_before + 1, test_player.steps)
        
        # edge cases
        # set object state
        test_player.position = 0
        steps_before = test_player.steps
        # execute method
        test_player.move_player(LEFT)
        # assert expected outcome
        self.assertEqual(0, test_player.position)
        self.assertEqual(steps_before, test_player.steps)

        # set object state
        test_player.position = 6
        steps_before = test_player.steps
        # execute method
        test_player.move_player(RIGHT)
        # assert expected outcome
        self.assertEqual(6, test_player.position)
        self.assertEqual(steps_before, test_player.steps)
    
    def test_capture_figure(self):
        # set object state
        test_figure = figure.Figure()
        test_player = player.Player()
        # execute method
        test_player.capture_figure(test_figure)
        # assert expected outcome
        self.assertEqual(test_figure, test_player.captured_figure)
        self.assertEqual('full', test_player.status)
    
    def test_action(self):
        # set state
        # create player instance
        test_player = player.Player()
        # set player at position 0
        test_player.position = 0
        # create column list
        column_list = [column.Column()]     # position 0
        # dictionary of coordinates returned by action()
        ray_coords = {
            'position': 0,  # player's position in the board (column number)
            'top': 0,  # where the first figure in that column starts, in pixels
            'x': 0,  # pixel number of x coordinate for ray start
            'y': 0,  # pixel number of x coordinate for ray start
            'c': 0  # counter
        }
        # test empty player, full column
        column_list[0].figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]     # 10 elements == full column
        test_player.status = 'empty'
        coords = test_player.action(column_list)
        self.assertNotEqual(ray_coords, coords)
        # test empty player, empty column
        column_list[0].figures = []  # 10 elements == full column
        test_player.status = 'empty'
        coords = test_player.action(column_list)
        self.assertEqual(ray_coords, coords)
        # test empty player, normal column
        column_list[0].figures = [0, 1, 2, 3, ]  # 10 elements == full column
        test_player.status = 'empty'
        coords = test_player.action(column_list)
        self.assertNotEqual(ray_coords, coords)
        # test full player, full column
        column_list[0].figures = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # 10 elements == full column
        test_player.status = 'full'
        coords = test_player.action(column_list)
        self.assertEqual(ray_coords, coords)
        # test full player, empty column
        column_list[0].figures = []  # 10 elements == full column
        test_player.status = 'full'
        coords = test_player.action(column_list)
        self.assertNotEqual(ray_coords, coords)
        # test full player, normal column
        column_list[0].figures = [0, 1, 2, 3, 4, 5, ]  # 10 elements == full column
        test_player.status = 'full'
        coords = test_player.action(column_list)
        self.assertNotEqual(ray_coords, coords)
        # TODO: assert more exacting results
    
    def test_empty(self):
        # set context
        test_figure = figure.Figure()
        test_player = player.Player()
        test_player.captured_figure = test_figure
        # execute method
        test_player.empty()
        # assert expected outcome
        self.assertIsNone(test_player.captured_figure)
        self.assertEqual('empty', test_player.status)
    
    def test_reset(self):
        # set context
        test_player = player.Player()
        test_player.status = 'qerqewr'
        test_player.online = 'qerqewr'
        test_player.score = 5
        test_player.steps = 6
        # execute method
        test_player.reset()
        # assert expected outcome
        self.assertIsNone(test_player.captured_figure)
        self.assertEqual('empty', test_player.status)
        self.assertEqual('', test_player.online)
        self.assertEqual(0, test_player.score)
        self.assertEqual(0, test_player.steps)

    def test_get_stats(self):
        # set context
        test_player = player.Player()
        test_stats = {
            'id': test_player.ID,  # random string that identifies player in server
            'name': test_player.name,  # name chosen by player
            'status': test_player.status,  # status of the game's character
            'score': test_player.score}
        # execute method
        results = test_player.get_stats()
        # assert expected outcome
        self.assertEqual(test_stats, results)


class TestMQ(unittest.TestCase):

	test_mq = None

	def __init__(self, *args, **kwargs):
		super(TestMQ, self).__init__(*args, **kwargs)
		pass
	
	def test_start(self):
		# set state
		host = 'qwerqew'
		topic = 'asfdadsf'
		
		test_mq = zmq_client.ZmqConnector()
		
		test_mq.client_auth = mock.Mock()
		test_mq.connect_push = mock.Mock()
		test_mq.connect_sub = mock.Mock()
		test_mq.filter_sub_socket = mock.Mock()
		test_mq.check_folder_structure = mock.Mock()
		test_mq.check_folder_structure.return_value = True
		
		# execute method
		test_mq.start(host, topic)
		
		# assert expected results
		self.assertTrue(test_mq.client_auth.called)
		self.assertTrue(test_mq.connect_push.called)
		self.assertTrue(test_mq.connect_sub.called)
		self.assertTrue(test_mq.filter_sub_socket.called)
		self.assertEqual(test_mq.host, host)
		self.assertIsNotNone(test_mq.context)
	
	def test_send(self):
		# set state
		test_mq = zmq_client.ZmqConnector()
		test_mq.push_send_multi = mock.Mock()
		
		# execute method
		test_mq.send('sender', {"info": "nada"}, {})
		
		# assert expected outcome
		self.assertTrue(test_mq.push_send_multi.called)
	
	# def test_check_folder_structure(self):
	# 	# TODO: find workaround issue with disparate cwd's affecting file and folder read
	# 	# set object state
	# 	test_mq = zmq_client.ZmqConnector()
	# 	test_mq.base_dir = ''
	# 	# execute method
	# 	result = test_mq.check_folder_structure()
	# 	# assert expected outcome
	# 	self.assertIsNotNone(result)
	# 	self.assertTrue(result)

	def test_disconnect(self):
		# set state
		test_mq = zmq_client.ZmqConnector()
		test_mq.context = mock.Mock()
		test_mq.pusher = mock.Mock()
		test_mq.subscriber = mock.Mock()
		
		# execute method
		test_mq.disconnect()
		
		# assert expected results
		self.assertTrue(test_mq.context.term.called)
		self.assertTrue(test_mq.pusher.close.called)
		self.assertTrue(test_mq.subscriber.close.called)
