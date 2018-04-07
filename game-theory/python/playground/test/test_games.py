# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from unittest import TestCase

import playground as play

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
