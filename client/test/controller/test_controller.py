import unittest
import sys
import os
from unittest import mock

sys.path.append(os.path.abspath('../../src/'))
from controller import controller
from model import figure, board


# TODO: find way to patch-in a mock pygame.event
class TestController(unittest.TestCase):
    
    test_ctrl = None
    
    def __init__(self, *args, **kwargs):
        super(TestController, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # check nulls
        self.assertIsNone(controller.Controller.view)
        self.assertIsNone(controller.Controller.player)
        self.assertIsNone(controller.Controller.FPSCLOCK)

        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        # execute method
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)

        # assert expected outcome
        self.assertIsNotNone(test_ctrl.targets)
        self.assertIsNotNone(test_ctrl.FPSCLOCK)
        self.assertEqual(mock_view, test_ctrl.view)
        self.assertEqual(mock_mq, test_ctrl.mq)
        self.assertEqual(mock_broker, test_ctrl.broker)
    
    def test_draw(self):
        # we test for every possible value of keyword
        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        # execute method
        inputs = test_ctrl.draw('start')
        # assert expected results
        self.assertIsNotNone(inputs)
        self.assertTrue(mock_view.draw_start_screen.called)
        # execute method
        inputs = test_ctrl.draw('game')
        # assert expected results
        self.assertIsNone(inputs)
        # execute method
        inputs = test_ctrl.draw('online_setup')
        # assert expected results
        self.assertIsNotNone(inputs)
        self.assertTrue(mock_view.draw_online_options_screen.called)
        test_ctrl.landing_data = [1, 2, b'{"hello": 1}']
        mock_player.name = 'my_player_name'
        # execute method
        inputs = test_ctrl.draw('landing_page')
        # assert expected results
        self.assertIsNotNone(inputs)
        self.assertTrue(mock_view.draw_landing_screen.called)
        # execute method
        inputs = test_ctrl.draw('find_online_match')
        # assert expected results
        self.assertIsNone(inputs)
        self.assertTrue(mock_view.draw_wait_screen.called)
        # execute method
        inputs = test_ctrl.draw('settings')
        # assert expected results
        self.assertIsNotNone(inputs)
        self.assertTrue(mock_view.draw_settings_screen.called)
        # execute method
        inputs = test_ctrl.draw('confirm_exit')
        # assert expected results
        self.assertIsNotNone(inputs)
        self.assertTrue(mock_view.confirm_exit.called)
        # execute method
        inputs = test_ctrl.draw('confirm_leave')
        # assert expected results
        self.assertIsNotNone(inputs)
        self.assertTrue(mock_view.confirm_leave_game.called)
        # execute method
        inputs = test_ctrl.draw('game_over')
        # assert expected results
        self.assertIsNone(inputs)
        self.assertTrue(mock_view.draw_game_over.called)
        # execute method
        inputs = test_ctrl.draw('victory')
        # assert expected results
        self.assertIsNone(inputs)
        self.assertTrue(mock_view.draw_victory.called)
    
    # EVENT LISTENERS: figure out way to mock pygame.event
    
    # GAMING METHODS
    
    def test_game_handler(self):
        # TODO: assert execution of test_ctrl own methods with
        # test for player.status: capturing/returning and all_targets_acquired True
        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        mock_board = mock.Mock()
        mock_board.longest_column_count = 3
        test_ctrl.board = mock_board
        mock_player.steps = 5
        test_ctrl.opponent = "opponent_me"
        # set player status
        # execute method
        test_ctrl.game_handler()
        # assert expected outcome
        self.assertTrue(mock_board.update_counts.called)
        self.assertTrue(mock_view.update_game_screen.called)
    
    def test_capture_animation(self):
        """
        execution scenarios:
        - self.view.animate_return(self.ray_coords): True/False
        """
        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_player.capture_figure.return_value = figure.Figure()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        test_ctrl.board = board.Board()
        test_ctrl.ray_coords = {'position': 3}
        
        # setup scenario
        mock_view.animate_return.return_value = False
        # execute method
        test_ctrl.capture_animation()
        # assert expected results
        self.assertTrue(mock_view.animate_return.called)
        self.assertTrue(mock_player.capture_figure.called)
        
        # setup scenario
        mock_player = mock.Mock()       # reset mock player
        test_ctrl.player = mock_player
        mock_view = mock.Mock()         # reset mock view
        test_ctrl.view = mock_view
        mock_view.animate_return.return_value = True
        # execute method
        test_ctrl.capture_animation()
        # assert expected results
        self.assertTrue(mock_view.animate_return.called)
        self.assertFalse(mock_player.capture_figure.called)
    
    def test_return_animation(self):
        """
        execution scenarios:
        - self.view.animate_return(self.ray_coords): True/False
        - len(self.board.columns[self.ray_coords['position']].figures) == 0
        - self.board.columns[self.ray_coords['position']].figures[-1].fits(self.player.captured_figure) == True
            - self.board.columns[self.ray_coords['position']].figures[-1].empty is True

        """
        # set object state
        mock_view = mock.Mock()
        mock_view.animate_return.return_value = False
        mock_player = mock.Mock()
        mock_player.capture_figure.return_value = figure.Figure()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        test_ctrl.board = board.Board()
        test_ctrl.ray_coords = {'position': 3}
        
        # setup scenario
        mock_view.animate_return.return_value = True
        # execute method
        test_ctrl.return_animation()
        # assert expected results (nothing happens)
        # TODO: actual assertions
        # setup scenario
        mock_view.animate_return.return_value = False
        # execute method
        test_ctrl.return_animation()
        # assert expected results
    
    def test_explode_all_targets(self):
        """
        execution scenarios:
        - self.frame < 16
        """
        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_player.score = 10
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        mock_board = mock.Mock()
        mock_board.eliminate_targets.return_value = 1
        test_ctrl.board = mock_board
        
        # setup scenario
        test_ctrl.frame = 15
        # execute method
        test_ctrl.explode_all_targets()
        # assert expected results
        self.assertTrue(mock_view.draw_explosion.called)
        self.assertEqual(test_ctrl.frame, 16)
        
        # setup scenario frame == 16
        # execute method
        test_ctrl.explode_all_targets()
        # assert expected results
        self.assertTrue(mock_view.draw_explosion.called)
        self.assertEqual(test_ctrl.frame, 0)
        self.assertTrue(mock_board.eliminate_targets.called)
    
    def test_update_match_state(self):
        """
        execution scenarios:
        - player.steps > 15
        - self.board.longest_column_count >= 10
        """
        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        
        mock_board = mock.Mock()
        test_ctrl.board = mock_board
        
        # setup scenario
        mock_player.steps = 16
        mock_board.longest_column_count = 10
        # execute method
        test_ctrl.update_match_state()
        # assert expected results
        self.assertTrue(mock_board.add_row.called)
        self.assertEqual(mock_player.steps, 0)
        self.assertEqual(test_ctrl.keyword, 'game_over')
        self.assertTrue(test_ctrl.draw_again)

        # setup scenario
        mock_player = mock.Mock()
        mock_player.steps = 15
        test_ctrl.player = mock_player
        mock_board = mock.Mock()
        mock_board.longest_column_count = 9
        test_ctrl.board = mock_board
        test_ctrl.keyword = ''
        test_ctrl.draw_again = False
        # execute method
        test_ctrl.update_match_state()
        # assert expected results
        self.assertFalse(mock_board.add_row.called)
        self.assertNotEqual(mock_player.steps, 0)
        self.assertNotEqual(test_ctrl.keyword, 'game_over')
        self.assertFalse(test_ctrl.draw_again)
    
    # ONLINE METHODS
    
    def test_find_match(self):
        """
        execution scenarios:
        - opponent None
            - player.online == 'available'/'ready'
        - opponent not none
        """
        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        mock_mq = mock.Mock()
        mock_broker = mock.Mock()
        test_ctrl = controller.Controller(mock_view, mock_player, mock_mq, mock_broker)
        
        # setup scenario
        mock_broker.negotiate_match.return_value = None
        mock_player.online = 'available'
        # execute method
        test_ctrl.find_match()
        # assert expected results
        self.assertEqual(test_ctrl.txt_msg, 'Waiting for challengers')

        # setup scenario
        mock_broker.negotiate_match.return_value = None
        mock_player.online = 'ready'
        # execute method
        test_ctrl.find_match()
        # assert expected results
        self.assertEqual(test_ctrl.txt_msg, 'Get ready to start')

        # setup scenario
        mock_broker.negotiate_match.return_value = 'opponent_me'
        # execute method
        test_ctrl.find_match()
        # assert expected results
        self.assertEqual(test_ctrl.opponent, 'opponent_me')
        self.assertEqual(mock_player.online, 'playing')
        self.assertEqual(test_ctrl.keyword, 'game')
        self.assertTrue(test_ctrl.draw_again)
        self.assertIsNotNone(test_ctrl.board)

        
if __name__ == '__main__':
    unittest.main()
