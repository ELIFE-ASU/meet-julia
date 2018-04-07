# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
"""
.. testsetup::

    from playground.games import *
"""
import numpy as np

class TwoPlayerGame(object):
    """
    The `TwoPlayerGame` type represents a two-player game using a
    :math:`2\\times2` payoff matrix. Aside from the shape, the payoff matrix is
    unconstrained.

    The `TwoPlayerGame` provides the root of a hierarchy of two-player games.
    Derived classes will impose constraints upon the payoff to ensure they
    conform to specific game structures.
    """
    def __init__(self, payoff):
        """
        Construct a `TwoPlayerGame` from a payoff matrix.

        .. doctest::

            >>> g = TwoPlayerGame([[0,1],[1,0]])
            >>> g.payoff
            array([[0., 1.],
                   [1., 0.]])
            >>> TwoPlayerGame([])
            Traceback (most recent call last):
            ...
            ValueError: payoff must have shape (2,2); got (0,)

        :param payoff: the payoff matrix
        :raises ValueError: if `payoff` is not :math:`2\\times2`
        """
        self.payoff = np.asarray(payoff, dtype=np.float64)
        shape = self.payoff.shape
        if shape != (2,2):
            msg = 'payoff must have shape (2,2); got {}'.format(shape)
            raise ValueError(msg)

    def __getitem__(self, index):
        """
        Access the elements of the payoff matrix.

        .. doctest::

            >>> g = TwoPlayerGame([[0,1],[2,3]])
            >>> g[0,1]
            1.0
            >>> g[-1,-2]
            2.0
            >>> g[2,1]
            Traceback (most recent call last):
            ...
            IndexError: index 2 is out of bounds for axis 0 with size 2kkk

        :param index: the index at which to access
        :raises IndexError: if the index is out of range
        """
        i, j = index
        return self.payoff[i,j]
