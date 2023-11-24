# testA.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main
from play_game import Game

class TestMainFunctions(unittest.TestCase):
    @patch('main.DATABASE', ':memory:')
    def setUp(self):
        main.init_db()

    def tearDown(self):
        pass

    @patch('main.execute_db_query')
    def test_load_topics_from_db(self, mock_execute):
        mock_execute.return_value = [(1, 'Science'), (2, 'Math')]
        result = main.load_topics_from_db()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], 'Science')
        self.assertEqual(result[1][1], 'Math')


if __name__ == '__main__':
    unittest.main()
