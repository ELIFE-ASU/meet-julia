# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
"""
.. testsetup::

    from playground import *
"""
from .games import TwoPlayerGame

class Playground(object):
    """
    A `Playground` is a network of agents competing against one another in a
    game. Each agent competes with its neighbors one-on-one and receives a
    payoff equal to the sum of the payoffs from each competition. The results
    from each round of competition are used to update each agent's strategy.
    """
    def __init__(self, game):
        """
        Construct a `Playground` from a game.

        .. doctest::

            >>> g = PrisonersDilemma(0.25, 0.75)
            >>> p = Playground(g)
            >>> type(p.game)
            <class 'playground.games.PrisonersDilemma'>

        :param game: the two-player game
        :type game: `np.ndarray` or `TwoPlayerGame`
        """
        if not isinstance(game, TwoPlayerGame):
            game = TwoPlayerGame(game)
        self.game = game
