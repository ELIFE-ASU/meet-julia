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
    def setUp(self):
        """
        Setup the test class with a random number generator
        """
        self.rng = np.random.RandomState(2018)

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

        payoff = np.empty((4,2), dtype=np.float64)
        p.payoff([0,1,0,1], payoff)
        self.assertTrue(np.array_equal(payoff,
            [[0.75,1.25], [1.5,2.], [0.75,1.5], [0.75,1.]]))

    def test_deterministic_update(self):
        """
        Ensure that we can synchronously update the agents' strategies using
        a deterministic rule.
        """
        game = HawkDove(0.25, 0.75)

        graph = nx.Graph()
        graph.add_nodes_from(range(4))
        graph.add_edges_from([(0,1), (0,2), (1,2), (2,3)])

        # Deterministic update
        rule = lambda p0, p1 : 0.0 if p1 <= p0 else 1.0

        p = Playground(game, graph, rule)

        state = [0,0,0,0]
        next_state = p.update(state, rng=self.rng)
        self.assertTrue(np.array_equal(next_state, [1,1,1,1]))

        p.update(next_state, next_state, rng=self.rng)
        self.assertTrue(np.array_equal(next_state, [0,0,0,0]))

        state = next_state
        next_state = np.zeros(len(next_state), dtype=np.int)
        p.update(state, next_state, rng=self.rng)
        self.assertTrue(np.array_equal(next_state, [1,1,1,1]))

    def test_timeseries(self):
        """
        Ensure that we can generate a timeseries of strageties.
        """
        game = StagHunt(0.25, 0.75)
        graph = nx.Graph()
        graph.add_nodes_from(range(4))
        graph.add_edges_from([(0,1), (0,2), (1,2), (2,3)])
        rule = lambda p0, p1 : 0.0 if p1 <= p0 else 1.0
        p = Playground(game, graph, rule)

        series = p.timeseries([0,1,0,1], 4);
        print(series)
        expect = [[0,1,0,1], [0,0,1,0], [0,0,0,1], [0,0,0,0], [0,0,0,0]]
        self.assertTrue(np.array_equal(series, expect))

        series = p.timeseries([1,1,1,1], 2);
        expect = [[1,1,1,1], [1,1,1,1], [1,1,1,1]]
        self.assertTrue(np.array_equal(series, expect))

        series = p.timeseries([1,0,1,1], 3);
        expect = [[1,0,1,1], [0,1,1,1], [1,0,1,1], [0,1,1,1]]
        self.assertTrue(np.array_equal(series, expect))
