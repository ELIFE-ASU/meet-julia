# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from unittest import TestCase

from playground import *

class TestPlayground(TestCase):
    """
    The `TestPlayground` class provides a suite of tests to validate the
    `Playground` class.
    """
    def test_canary(self):
        """
        Ensure the shaft isn't filling with carbon dioxide.
        """
        self.assertEqual(1 + 2, 3)

    def test_invalid_game(self):
        """
        Constructing a playground with an invalid game raises an `ValueError`.
        """
        with self.assertRaises(ValueError):
            Playground([])

        with self.assertRaises(ValueError):
            Playground([1,2])

        with self.assertRaises(ValueError):
            Playground([[1,2]])

        with self.assertRaises(ValueError):
            Playground([[1,2],[3,4],[5,6]])

        with self.assertRaises(ValueError):
            Playground([[1,2,3],[4,5,6]])

    def test_valid_playground(self):
        """
        Ensure that we can properly construct a playground
        """
        p = Playground(PrisonersDilemma(0.25,0.75))
        self.assertTrue(np.array_equal(p.game.payoff, [[0.75,0.0],[1.0,0.25]]))
