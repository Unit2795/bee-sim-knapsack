import math
import random
import time
import os

from flowers import hundred_flower_meadow as avail_flowers
from helpers import print_info_message, print_in_color, MessageColor, print_matrix


class BeeSimulator:
    # Initialize the BeeSimulator with the game config (available flowers and the bee's energy)
    def __init__(self, sim_speed=None, bee_energy=100, game_map=avail_flowers):
        # Initialize the game map with the available flowers
        self.flowers = game_map
        # Bee energy is akin to the weight limit of the knapsack problem
        self.bee_energy = bee_energy
        self.sim_speed = sim_speed if sim_speed is not None else int(os.environ.get("SPEED", 1))
        # Initialize the dynamic programming table used for memoization
        # Columns represent the bee's energy and the rows represent the flowers
        # -1 denotes an uncomputed value
        self.total_flowers = len(game_map)
        self.dp = [[-1] * (bee_energy + 1) for _ in range(self.total_flowers)]
        self.collected_flowers = []
        self.max_nectar = 0


    # Start the bee simulation
    def start(self):
        # Call the bee simulator function to find the optimal solution
        self.max_nectar = self._max_nectar_recursive(self.flowers, self.total_flowers - 1, self.bee_energy)
        # Trace back the choices made to determine which flowers will actually be collected by the bee
        self._traceback(self.flowers, self.bee_energy)

        # Print the DP and trace back table if logging is enabled
        print_matrix(self.dp, "Dynamic Programming Table")

        # Begin the game loop
        self._play_simulation()

        return self.max_nectar

    # Main game loop to simulate the bee collecting nectar from flowers
    def _play_simulation(self):
        print_in_color(
            f"☀️ Your bee has woken up in a beautiful meadow on a sunny day and is ready to start collecting nectar! 🌻",
            MessageColor.YELLOW)
        self._game_loop()
        print_in_color(
            "🌙 The day is over and your bee is sleepy, they have returned to the hive for a good night's rest... 💤",
            MessageColor.BLUE)
        # Print the final result of the simulation
        print_in_color(f"Total nectar collected by your bee: {self.max_nectar}. Great Job! ⭐", MessageColor.MAGENTA)

    # Main game loop to simulate the bee collecting nectar from flowers
    def _game_loop(self):
        for flower in self.collected_flowers:
            # Simulate the bee collecting nectar from the flower by sleeping for a random amount of time
            # The delay is proportional to the energy cost of the flower and is a random value between half and the full energy cost in seconds
            if self.sim_speed != 0:
                delay: int = math.ceil(random.uniform(flower[2] / 2, flower[2]))
                time.sleep(delay * self.sim_speed)
            print_in_color(
                f"Bee collected {flower[1]} nectar from a {flower[0]}, expending {flower[2]} energy. (Total Nectar: {flower[4]}) (Remaining Energy: {flower[3]})",
                MessageColor.GREEN)

    # Trace back the choices made to determine which flowers were actually collected by the bee
    def _traceback(self, flowers, bee_energy):
        # Start the bee with no collected flowers and maximum energy
        energy = bee_energy
        total_nectar = 0

        # Start in the bottom right corner of the choices table
        for flower in reversed(range(len(flowers))):
            # If the bee chose to collect the current flower, it is part of the optimal solution
            if self.dp[flower][energy] != -1 and (flower == 0 or self.dp[flower][energy] != self.dp[flower - 1][energy]):
                total_nectar += flowers[flower].nectar
                flower_info = (flowers[flower].name, flowers[flower].nectar, flowers[flower].energy_cost, energy, total_nectar, flower)
                self.collected_flowers.append(flower_info)

                # Move the bee's energy to the left by the energy cost of the flower
                # We'll keep evaluating from here until the bee is out of energy or there are no more flowers
                energy -= flowers[flower].energy_cost

    # Primary recursive function to find the maximum nectar the bee can collect (Knapsack Problem Algorithm)
    def _max_nectar_recursive(self, flowers, flower_index, bee_energy):
        # BASE CASE: The bee has no more energy (columns) or there are no more flowers to visit (rows).
        # If you were writing the DP table by hand, this would be the first row and column.
        if bee_energy <= 0 or flower_index < 0:
            return 0

        # If the current cell in the DP table has already been calculated (memoized), return the value.
        if self.dp[flower_index][bee_energy] != -1:
            return self.dp[flower_index][bee_energy]

        # Select the current flower we will be evaluating
        current_flower = flowers[flower_index]

        # If the current flower's energy cost is greater than the bee's remaining energy,
        # we skip this flower and move on to the next.
        if current_flower.energy_cost > bee_energy:
            print_info_message(
                f"Skipping {current_flower.name} due to high energy cost. Needed Energy: {current_flower.energy_cost}. Available energy: {bee_energy}. Deficit: {bee_energy - current_flower.energy_cost}  (Row: {flower_index}, Column: {bee_energy})")
            result = self._max_nectar_recursive(flowers, flower_index - 1, bee_energy)
        else:
            # Perform a comparison between two scenarios:
            # 1. The bee collects the nectar and pollen from the current flower
            # 2. The bee skips the current flower and moves on to the next one
            # The optimal solution is the maximum nectar value of these two scenarios.
            collect = current_flower.nectar + self._max_nectar_recursive(flowers, flower_index - 1,
                                                                         bee_energy - current_flower.energy_cost)
            not_collect = self._max_nectar_recursive(flowers, flower_index - 1, bee_energy)
            result = max(collect, not_collect)

            # Print information about the current flower and the decision-making process
            decision = "COLLECT" if collect > not_collect else "SKIP"
            print_info_message(f"""
            Considering {current_flower.name} (Row: {flower_index}, Column: {bee_energy})
                {current_flower.nectar} (+{current_flower.nectar} nectar), {current_flower.energy_cost} (-{current_flower.energy_cost} energy), 
                New total nectar if collected: {collect}
                New total nectar if SKIPPED: {not_collect}
                {result} (MAX of {collect} and {not_collect})
                Decision: {decision}
            """)

        # Store the result in the DP table for future reference
        self.dp[flower_index][bee_energy] = result
        return result
