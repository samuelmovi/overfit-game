import unittest
import sys
import os
sys.path.append(os.path.abspath('../../src/'))
from model import player, figure


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
    
    # def test_action(self):
    #     # set object state
    #     # set player status empty/full
    #     # create test column
    #     # execute method
    #
    #     # assert expected outcome
    #
    #     pass
    
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
        # execute method
        test_player.reset()
        # assert expected outcome
        self.assertIsNone(test_player.captured_figure)
        self.assertEqual('empty', test_player.status)
        self.assertEqual('', test_player.online)
        self.assertEqual(0, test_player.score)
        self.assertEqual(0, test_player.steps)
        self.assertFalse(test_player.connected)

    def test_get_stats(self):
        # set context
        test_player = player.Player()
        test_stats = {
            'sender': test_player.ID,  # random string that identifies player in server
            'name': test_player.name,  # name chosen by player
            'online': test_player.online,  # player's online status
            'status': test_player.status,  # status of the game's character
            'score': test_player.score}
        # execute method
        results = test_player.get_stats()
        # assert expected outcome
        self.assertEqual(test_stats, results)
        

if __name__ == '__main__':
    unittest.main()
