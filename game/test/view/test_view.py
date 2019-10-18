import unittest
import sys
import os
sys.path.append(os.path.abspath('../../'))
from view import view
from controller import controller
import pygame


class TestView(unittest.TestCase):
    base_dir = os.getcwd()
    
    def __init__(self, *args, **kwargs):
        super(TestView, self).__init__(*args, **kwargs)
        pygame.init()
        self.test_view = view.View()
        self.test_view.base_dir = os.path.join(os.getcwd(), '../../')
        # could use a mock surface object to replace screen
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

    def test_draw_online_options_screen(self):
        # set object state
        self.test_view.set_up_fonts()
        # execute method
        results = self.test_view.draw_online_options_screen("player_name", "host_ip")
        # assert expected outcome
        for result in results:
            self.assertIsNotNone(result)
    
    def test_draw_settings_screen(self):
        # set object state
        self.test_view.set_up_fonts()
        # execute method
        results = self.test_view.draw_settings_screen("player_name", "host_ip")
        # assert expected outcome
        for result in results:
            self.assertIsNotNone(result)
    
    def test_animate_capture(self):
        # set object state
        ray_coords = dict()
        ray_coords['top'] = 100
        ray_coords['x'] = 10
        ray_coords['y'] = 200
        ray_coords['c'] = 10
        controller.Controller.load_external_resources(self.test_view, os.path.join(os.getcwd(), '../../'))
        
        # execute method
        outcome = self.test_view.animate_capture(ray_coords)
        # assert expected outcome
        self.assertTrue(outcome)
        
        # reset data
        ray_coords['y'] = 10
        # execute method
        outcome = self.test_view.animate_capture(ray_coords)
        # assert expected outcome
        self.assertFalse(outcome)
        

if __name__ == '__main__':
    unittest.main()
