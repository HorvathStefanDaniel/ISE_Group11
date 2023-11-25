# test_gui.py
import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

class TestGUICreation(unittest.TestCase):

    @patch('main.tk.Canvas')
    @patch('main.tk.Button')
    def test_main_menu_buttons(self, mock_button, mock_canvas):
        # Mock the root window and configure it to return integers for screen dimensions
        root = MagicMock()
        root.winfo_screenwidth.return_value = 1920
        root.winfo_screenheight.return_value = 1080
        main.root = root

        # Mock the canvas creation and return a mock canvas object
        mock_canvas.return_value = MagicMock()

        # Call the function that should create the buttons
        main.create_main_menu()

        # The create_window method should be called on the mock canvas object
        self.assertTrue(mock_canvas.return_value.create_window.called)

        # Check if Button was called with the "HOW TO PLAY" text and a command function
        how_to_play_calls = [args for args, kwargs in mock_button.call_args_list if kwargs.get('text') == "HOW TO PLAY"]
        self.assertTrue(how_to_play_calls)
        self.assertTrue(any('command' in kwargs for args, kwargs in mock_button.call_args_list if kwargs.get('text') == "HOW TO PLAY"))

if __name__ == '__main__':
    unittest.main()
