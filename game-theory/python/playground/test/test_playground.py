# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.
from unittest import TestCase

import playground as play

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
