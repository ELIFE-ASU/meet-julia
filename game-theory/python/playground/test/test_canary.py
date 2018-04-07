# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from unittest import TestCase

import playground as play

class TestCanary(TestCase):
    """
    The `TestCanary` class provides a simple sentinal_ test class to ensure that
    the unit testing suite is working properly.

    .. _sentinal: https://en.wikipedia.org/wiki/Sentinel_species
    """

    def test_add_one_two(self):
        """
        Ensure that :math:`1 + 2 = 3`.
        """
        self.assertEqual(1 + 2, 3)
