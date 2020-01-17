import unittest
import sys
import os
from unittest.mock import Mock

sys.path.append(os.path.abspath('../src/'))
import db_controller


class TestDB(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)
        pass
    
    def test_init(self):
        pass
    
    def test_populate_db(self):
        pass
    
    def test_load_matches(self):
        pass
    
    def test_save_match(self):
        pass
    

if __name__ == '__main__':
    unittest.main()
