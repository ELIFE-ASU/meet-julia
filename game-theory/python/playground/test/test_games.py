# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from unittest import TestCase

import playground as play
import numpy as np

class TestGames(TestCase):
    """
    The `TestGames` class provides a suite of tests for the class hierarchy of
    two player games.
    """
    def test_canary(self):
        """
        Is there too much carbon monoxide in the air?
        """
        self.assertEqual(1 + 2, 3)

    def test_two_player_invalid_payoff(self):
        """
        Ensure that `TwoPlayerGame` raises a `ValueError` when the provided
        payoff matrix is invalid (i.e. not a 2x2 matrix).
        """
        with self.assertRaises(ValueError):
            play.TwoPlayerGame([])

        with self.assertRaises(ValueError):
            play.TwoPlayerGame([1,2])

        with self.assertRaises(ValueError):
            play.TwoPlayerGame([[1,2]])

        with self.assertRaises(ValueError):
            play.TwoPlayerGame([[1,2],[3,4],[5,6]])

        with self.assertRaises(ValueError):
            play.TwoPlayerGame([[1,2,3],[4,5]])

        with self.assertRaises(ValueError):
            play.TwoPlayerGame([[1,2,3],[4,5,6]])

    def test_two_player_init(self):
        """
        Ensure that the payoff matrix is properly assigned on construction of a
        `TwoPlayerGame`.
        """
        payoff = [[0.1, 0.2], [0.3, 0.4]]
        game = play.TwoPlayerGame(payoff)
        self.assertTrue(np.array_equal(payoff, game.payoff))
