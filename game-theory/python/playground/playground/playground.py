# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
"""
.. testsetup::

    from playground import *
    import networkx as nx
    from math import exp, tanh
"""
from .games import TwoPlayerGame

import numpy as np

class Playground(object):
    """
    A `Playground` is a network of agents competing against one another in a
    game. Each agent competes with its neighbors one-on-one and receives a
    payoff equal to the sum of the payoffs from each competition. The results
    from each round of competition are used to update each agent's strategy.
    """
    def __init__(self, game, graph, rule):
        """
        Construct a `Playground` from a game, graph and strategy update rule.

        .. doctest::

            >>> game = PrisonersDilemma(0.25, 0.75)
            >>> graph = nx.erdos_renyi_graph(n=4, p=0.25, seed=2018)
            >>> rule = lambda p_0, p_1 : 1.0
            >>> p = Playground(game, graph, rule)
            >>> type(p.game)
            <class 'playground.games.PrisonersDilemma'>
            >>> type(p.graph)
            <class 'networkx.classes.graph.Graph'>
            >>> type(p.rule)
            <type 'function'>

        :param game: the two-player game
        :type game: `np.ndarray` or `TwoPlayerGame`
        :param graph: the competition graph
        :param rule: the strategy update rule
        """
        if not isinstance(game, TwoPlayerGame):
            game = TwoPlayerGame(game)
        self.game = game
        self.graph = graph
        self.rule = rule
        self.number_of_agents = graph.number_of_nodes()

    def payoff(self, strategies, payoff=None):
        """
        Determine the potential payoff each agent might receive all possible
        strategies given its neighbors' current strategies. Each row of the
        resulting array corresponds to an agent, and each column a potential
        strategy.

        .. doctest::
        
            >>> game = PrisonersDilemma(0.25, 0.75)
            >>> graph = nx.erdos_renyi_graph(n=4, p=0.75, seed=2018)
            >>> rule = lambda p_0, p_1 : 1.0
            >>> p = Playground(game, graph, rule)
            >>> p.payoff([0,0,0,0])
            array([[2.25, 3.  ],
                   [2.25, 3.  ],
                   [2.25, 3.  ],
                   [2.25, 3.  ]])
            >>> p.payoff([0,1,1,0])
            array([[0.75, 1.5 ],
                   [1.5 , 2.25],
                   [1.5 , 2.25],
                   [0.75, 1.5 ]])

        :param strategies: the strategies of all of the agents
        :param payoff: (*optional*) an array into which the payoffs
        :return: the array of payoffs
        """
        if len(strategies) != self.number_of_agents:
            raise ValueError('strategies array as wrong number of strategies')

        if payoff is None:
            payoff = np.zeros((len(strategies), 2), dtype=np.float64)
        elif payoff.shape != (len(strategies), 2):
            raise ValueError('payoff is wrong shape')
        else:
            payoff[:,:] = 0.0

        game = self.game
        for i in range(self.number_of_agents):
            for j in self.graph.neighbors(i):
                y = strategies[j]
                payoff[i,:] += game[:,y]

        return payoff

    def update(self, strategies, next_strategies=None, rng=None):
        """
        Stochastically update the strategies according to the `Playground`'s
        `rule`. Each agent selects a new strategy based on the strategies of
        its neighbors at the current time step.

        .. doctest::

            >>> rng = np.random.RandomState(2018)
            >>> game = StagHunt(0.25, 0.75)
            >>> graph = nx.barabasi_albert_graph(n=10, m=2, seed=2018)
            >>> rule = lambda p0, p1 : 0.5 * (1 + tanh(p1 - p0))
            >>> p = Playground(game, graph, rule)
            >>> state = p.update(np.zeros(10, np.int), rng=rng)
            >>> state
            array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1])
            >>> state = p.update(state, rng=rng)
            >>> state
            array([0, 0, 0, 1, 0, 0, 0, 1, 0, 0])
            >>> p.update(state, state, rng=rng)
            array([0, 1, 0, 0, 0, 1, 1, 0, 0, 0])
            >>> state
            array([0, 1, 0, 0, 0, 1, 1, 0, 0, 0])

        """
        if next_strategies is None:
            next_strategies = np.empty(len(strategies), dtype=np.int)
        elif strategies.shape != next_strategies.shape:
            raise ValueError('strategies and next_strategies have different shapes')

        if rng is None:
            ts = np.random.rand(self.number_of_agents)
        else:
            ts = rng.rand(self.number_of_agents)

        payoff = self.payoff(strategies)

        rule = self.rule
        for i, p in enumerate(payoff):
            next_strategies[i] = (ts[i] <= rule(p[0], p[1]))

        return next_strategies
