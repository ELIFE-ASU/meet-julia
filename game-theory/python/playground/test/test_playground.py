# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from unittest import TestCase
from playground import *
import networkx as nx

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

    def test_playground_init(self):
        """
        Ensure that we can properly construct a playground
        """
        game = PrisonersDilemma(0.25,0.75)
        graph = nx.erdos_renyi_graph(20, 0.3, 2018)
        rule = lambda p0, p1 : 1
        p = Playground(game, graph, rule)
        self.assertTrue(np.array_equal(p.game.payoff, [[0.75,0.0],[1.0,0.25]]))
        self.assertEqual(p.graph, graph)
        self.assertEqual(p.rule, rule)

    def test_payoff(self):
        """
        Ensure that the pay is properly calculated given a set of strategies.
        """
        game = PrisonersDilemma(0.25, 0.75)
        graph = nx.Graph()
        graph.add_nodes_from(range(4))
        graph.add_edges_from([(0,1), (0,2), (1,2), (2,3)])
        rule = lambda p0, p1 : 1 / (1 + exp(p0 - p1))

        p = Playground(game, graph, rule)
        self.assertTrue(np.array_equal(p.payoff([0,0,0,0]),
            [[1.5,2.], [1.5,2.], [2.25,3.], [0.75,1.]]))

        self.assertTrue(np.array_equal(p.payoff([0,1,0,1]),
            [[0.75,1.25], [1.5,2.], [0.75,1.5], [0.75,1.]]))

        self.assertTrue(np.array_equal(p.payoff([1,1,1,1]),
            [[0.0,0.5], [0.0,0.5], [0.0,0.75], [0.0,0.25]]))
