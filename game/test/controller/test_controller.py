import unittest
import sys
import os
from unittest import mock

sys.path.append(os.path.abspath('../../src/'))
from controller import controller


class TestController(unittest.TestCase):
    
    test_ctrl = None
    
    def __init__(self, *args, **kwargs):
        super(TestController, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # check nulls
        self.assertIsNone(controller.Controller.my_view)
        self.assertIsNone(controller.Controller.player)
        self.assertIsNone(controller.Controller.FPSCLOCK)

        # set object state
        mock_view = mock.Mock()
        mock_player = mock.Mock()
        # execute method
        self.test_ctrl = controller.Controller(mock_view, mock_player)

        # assert expected outcome
        self.assertIsNotNone(self.test_ctrl.targets)
        self.assertIsNotNone(self.test_ctrl.FPSCLOCK)
        self.assertEqual(mock_view, self.test_ctrl.my_view)
        self.assertEqual(mock_player, self.test_ctrl.player)

    # def test_capture_animation(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_return_animation(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_explode_all_targets(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_check_player_events(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_update_player_stats(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_check_online_play(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_check_on_opponent(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    #
    # def test_reset_state(self):
    #     # set object state
    #
    #     # execute method
    #
    #     # assert expected outcome
    #     pass
    
        
if __name__ == '__main__':
    unittest.main()
