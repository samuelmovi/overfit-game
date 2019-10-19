import unittest
import sys
import os
from ..src.game import Start

sys.path.append(os.path.abspath('../../src/'))
from .controller import controller
from .model import player
from .view import view


class TestStart(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStart, self).__init__(*args, **kwargs)
        self.test_start = None
        pass
    
    def test_main(self):
        # set object state
        # execute method
        self.test_start = Start()
        # assert expected outcome
        self.assertIsNone(self.test_start.my_player)
        self.assertIsNone(self.test_start.my_view)
        self.assertIsNone(self.test_start.ctrl)


if __name__ == '__main__':
    unittest.main()
