import unittest
import sys
import os

sys.path.append(os.path.abspath('../src/'))
import start


class TestStart(unittest.TestCase):
    
    # test the self.db, self.mq, and self.server not null
    
    def __init__(self, *args, **kwargs):
        super(TestStart, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        # set object state
        
        # execute method
        test_start = start.Start()
        # assert expected outcome
        # server and mq are none
        self.assertIsNone(test_start.mq)
        self.assertIsNone(test_start.mq)
        self.assertIsNone(test_start.server)


if __name__ == '__main__':
    unittest.main()
