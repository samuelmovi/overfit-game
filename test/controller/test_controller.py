import unittest
import sys
import os

sys.path.append(os.path.abspath('../../game/'))
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
        self.assertIsNone(controller.Controller.targets)
        self.assertIsNone(controller.Controller.FPSCLOCK)

        # set object state
        
        # execute method
        self.test_ctrl = controller.Controller()

        # assert expected outcome
        self.assertIsNotNone(controller.Controller.my_view)
        self.assertIsNotNone(controller.Controller.player)
        self.assertIsNotNone(controller.Controller.targets)
        self.assertIsNotNone(controller.Controller.FPSCLOCK)
        
        
if __name__ == '__main__':
    unittest.main()
