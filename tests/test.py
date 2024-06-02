import unittest
import logging
import numpy as np

from beesim import BeeSimulator
from flowers import tiny_meadow as tiny_meadow_map
from helpers import print_in_color, MessageColor
from tests.references import get_matrices

logging.basicConfig(level=logging.INFO)


class TestBeeSimulator(unittest.TestCase):
    def test_tiny_meadow(self):
        bee_sim = BeeSimulator(0, 10, tiny_meadow_map)

        max_nectar = bee_sim.start()

        # Maximum nectar that can be collected is 26
        self.assertEqual(max_nectar, 26)

        print_in_color("Tiny Meadow DP Table:", MessageColor.BLUE)
        for row in bee_sim.dp:
            print(' '.join(map(str, row)))
        print_in_color("Tiny Meadow Traceback Table:", MessageColor.BLUE)
        for row in bee_sim.collected_flowers:
            print(' '.join(map(str, row)))
        print_in_color("INFO: If you need to update the reference matrices, run the update_matrices() function in tests/references.py, BUT ENSURE THE ABOVE TINY MEADOW TABLES ARE CORRECT FIRST!", MessageColor.RED)

    def test_hundred_meadow(self):
        dp, traceback = get_matrices()

        bee_sim = BeeSimulator(0)

        max_nectar = bee_sim.start()

        # Maximum nectar that can be collected is 279
        self.assertEqual(max_nectar, 279)

        np.testing.assert_array_equal(bee_sim.dp, dp)

        np.testing.assert_array_equal(bee_sim.collected_flowers, traceback)
