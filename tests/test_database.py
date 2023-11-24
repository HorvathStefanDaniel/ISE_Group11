# test_database.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

class TestDatabaseFunctions(unittest.TestCase):
    @patch('main.sqlite3.connect')
    def test_execute_db_query_select(self, mock_connect):
        # Set up the MagicMock to behave correctly in a context manager
        mock_conn = MagicMock()
        mock_connect.return_value = MagicMock(__enter__=MagicMock(return_value=mock_conn))
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ('Sample Row',)

        result = main.execute_db_query("SELECT * FROM table WHERE id=?", (1,), fetchall=False)
        self.assertEqual(result, ('Sample Row',))
        mock_cursor.execute.assert_called_with("SELECT * FROM table WHERE id=?", (1,))
        mock_cursor.fetchone.assert_called()

    @patch('main.sqlite3.connect')
    def test_execute_db_query_commit(self, mock_connect):
        # Set up the MagicMock to behave correctly in a context manager
        mock_conn = MagicMock()
        mock_connect.return_value = MagicMock(__enter__=MagicMock(return_value=mock_conn))
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 123

        result = main.execute_db_query("INSERT INTO table (column) VALUES (?)", ("value",), commit=True)
        self.assertEqual(result, 123)
        mock_cursor.execute.assert_called_with("INSERT INTO table (column) VALUES (?)", ("value",))
        mock_conn.commit.assert_called()

if __name__ == '__main__':
    unittest.main()
