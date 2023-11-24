# test_gui.py
import unittest
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

class TestGUICreation(unittest.TestCase):
    def test_create_rounded_button(self):
        canvas = MagicMock()
        main.create_rounded_button(canvas, 10, 10, 100, 50, 10, "Test", lambda: None)
        self.assertTrue(canvas.create_oval.called)
        self.assertTrue(canvas.create_rectangle.called)
        self.assertTrue(canvas.create_text.called)

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
