import unittest
import sys
import os
from unittest import mock

sys.path.append(os.path.abspath('../../src/'))
from controller import controller


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

    
if __name__ == '__main__':
    unittest.main()
