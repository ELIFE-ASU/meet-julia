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

    def test_two_player_getitem(self):
        """
        Ensure that `TwoPlayerGame.__getitem__` correctly accesses the payoff
        matrix.
        """
        g = play.TwoPlayerGame([[0,1],[2,3]])
        self.assertEqual(g[0,0], 0)
        self.assertEqual(g[0,1], 1)
        self.assertEqual(g[1,0], 2)
        self.assertEqual(g[1,1], 3)

        self.assertEqual(g[-1,-1], 3)

        with self.assertRaises(IndexError):
            g[2,0]

        with self.assertRaises(IndexError):
            g[-3,0]

    def test_prisoners_dilemma_derives(self):
        """
        Ensure that the `PrisonersDilemma` class derives from `TwoPlayerGame`.
        """
        self.assertTrue(issubclass(play.PrisonersDilemma, play.TwoPlayerGame))

    def test_prisoners_dilemma_invalid(self):
        """
        The strong prisoner's dilemma requires that :math:`1.0 > R > P > 0.0`.
        Ensure that an error is raised if this condition does not hold.
        """
        with self.assertRaises(ValueError):
            play.PrisonersDilemma(-0.5, 0.5)

        with self.assertRaises(ValueError):
            play.PrisonersDilemma(0.0, 0.5)

        with self.assertRaises(ValueError):
            play.PrisonersDilemma(0.5, 1.0)

        with self.assertRaises(ValueError):
            play.PrisonersDilemma(0.5, 1.5)

        with self.assertRaises(ValueError):
            play.PrisonersDilemma(0.75, 0.25)

    def test_prisoners_dilemma_init(self):
        """
        Ensure the PD payoff matrix is properly constructed.
        """
        g = play.PrisonersDilemma(0.25, 0.75)
        self.assertTrue(np.array_equal(g.payoff, [[0.75,0.0], [1.0,0.25]]))

    def test_hawk_dove_derives(self):
        """
        Ensure that the `HawkDove` class derives from `TwoPlayerGame`.
        """
        self.assertTrue(issubclass(play.HawkDove, play.TwoPlayerGame))

    def test_hawk_dove_invalid(self):
        """
        The strong hawk-dove game requires that :math:`1.0 > P > T > 0.0`.
        Ensure that an error is raised if this condition does not hold.
        """
        with self.assertRaises(ValueError):
            play.HawkDove(-0.5, 0.5)

        with self.assertRaises(ValueError):
            play.HawkDove(0.0, 0.5)

        with self.assertRaises(ValueError):
            play.HawkDove(0.5, 1.0)

        with self.assertRaises(ValueError):
            play.HawkDove(0.5, 1.5)

        with self.assertRaises(ValueError):
            play.HawkDove(0.75, 0.25)

    def test_hawk_dove_init(self):
        """
        Ensure the HD payoff matrix is properly constructed.
        """
        g = play.HawkDove(0.25, 0.75)
        self.assertTrue(np.array_equal(g.payoff, [[0.0, 1.0], [0.25, 0.75]]))

    def test_stag_hunt_derives(self):
        """
        Ensure that the `StagHunt` class derives from `TwoPlayerGame`.
        """
        self.assertTrue(issubclass(play.StagHunt, play.TwoPlayerGame))

    def test_stag_hunt_invalid(self):
        """
        The strong stag hunt game requires that :math:`1.0 > T > P > 0.0`.
        Ensure that an error is raised if this condition does not hold.
        """
        with self.assertRaises(ValueError):
            play.StagHunt(-0.5, 0.5)

        with self.assertRaises(ValueError):
            play.StagHunt(0.0, 0.5)

        with self.assertRaises(ValueError):
            play.StagHunt(0.5, 1.0)

        with self.assertRaises(ValueError):
            play.StagHunt(0.5, 1.5)

        with self.assertRaises(ValueError):
            play.StagHunt(0.75, 0.25)

    def test_stag_hunt_init(self):
        """
        Ensure the SH payoff matrix is properly constructed.
        """
        g = play.StagHunt(0.25, 0.75)
        self.assertTrue(np.array_equal(g.payoff, [[1.0, 0.0], [0.75, 0.25]]))
