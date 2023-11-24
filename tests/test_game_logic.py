# test_game_logic.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust the path to include the parent directory, so we can import modules from there
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Game and GameSetup from the correct module
from play_game import Game, GameSetup

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.root = MagicMock()
        self.on_main_menu = MagicMock()
        self.on_game_start = MagicMock()

    def test_game_setup_initialization(self):
        game_setup = GameSetup(self.root, self.on_game_start, self.on_main_menu)
        # Check if UI elements of GameSetup are initialized properly
        self.assertIsNotNone(game_setup.topic_listbox)
        self.assertIsNotNone(game_setup.player_number_spinbox)

    def test_game_initialization(self):
        # Create a mock for Game class
        game = Game(self.root, self.on_main_menu, ['Science'], 2)
        # Check if the game initializes with correct number of players and their scores
        self.assertEqual(game.number_of_players, 2)
        self.assertIn('Player 1', game.players_scores)
        self.assertIn('Player 2', game.players_scores)

    # Additional tests for game logic can be added here

if __name__ == '__main__':
    unittest.main()
