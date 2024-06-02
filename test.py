import unittest

from beesim import BeeSimulator


class TestBeeSimulator(unittest.TestCase):
    def test_hundred_meadow(self):
        bee_sim = BeeSimulator(0)

        # Maximum nectar that can be collected is 279
        self.assertEqual(bee_sim.start(), 279)

