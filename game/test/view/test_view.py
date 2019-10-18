import unittest
import sys
import os
sys.path.append(os.path.abspath('../../'))
from view import view
import pygame


class TestView(unittest.TestCase):
    base_dir = os.getcwd()
    
    def __init__(self, *args, **kwargs):
        super(TestView, self).__init__(*args, **kwargs)
        pygame.init()
        self.test_view = view.View()
        self.test_view.base_dir = os.path.join(os.getcwd(), '../../')
        pass

    def test_init(self):
        # set object state
        
        # execute method
        
        # assert expected outcome
        self.assertIsNotNone(self.test_view.screen)

    def test_draw_start_screen(self):
        # set object state
        self.test_view.set_up_fonts()
        # execute method
        results = self.test_view.draw_start_screen()
        # assert expected outcome
        for result in results:
            self.assertIsNotNone(result)

    
if __name__ == '__main__':
    unittest.main()
