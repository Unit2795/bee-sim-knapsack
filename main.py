from flowers import Flower, flowers as avail_flowers
from helpers import printMatrix


def bee_simulator(flowers, flower_index, bee_energy, dp, total_flowers):
    # BASE CASE: The bee has no more energy (columns) or there are no more flowers to visit (rows).
    # If you were writing the DP table by hand, this would be the first row and column.
    if bee_energy <= 0 or flower_index >= total_flowers:
        return 0

    # If the current cell in the DP table has already been calculated (memoized), return the value.
    if dp[flower_index][bee_energy] != 0:
        return dp[flower_index][bee_energy]

    # Select the current flower we will be evaluating
    current_flower = flowers[flower_index]

    # If the current flower's energy cost is greater than the bee's remaining energy,
    # we skip this flower and move on to the next.
    if current_flower.energy_cost > bee_energy:
        return bee_simulator(flowers, flower_index + 1, bee_energy, dp, total_flowers)
    else:
        # Perform a comparison between two scenarios:
        # 1. The bee collects the nectar and pollen from the current flower
        # 2. The bee skips the current flower and moves on to the next one
        # The optimal solution is the maximum nectar value of these two scenarios.
        collect = current_flower.nectar + bee_simulator(flowers, flower_index + 1,
                                                        bee_energy - current_flower.energy_cost, dp, total_flowers)
        not_collect = bee_simulator(flowers, flower_index + 1, bee_energy, dp, total_flowers)

        result = max(collect, not_collect)
        # Store the result in the DP table for future reference
        dp[flower_index][bee_energy] = result
        return result


# Initialize parameters for the bee simulator and call the function
def main():
    # Bee energy is akin to the weight limit of the knapsack problem
    bee_energy = 10

    # Initialize the dynamic programming table used for memoization
    # Columns represent the bee's energy and the rows represent the flowers
    dp = [[0] * (bee_energy + 1) for _ in range(len(avail_flowers))]

    total_flowers = len(avail_flowers)

    # Call the bee simulator function to find the optimal solution
    result = bee_simulator(avail_flowers, 0, bee_energy, dp, total_flowers)

    print(f"Maximum nectar and pollen collected by the bee: {result}")
    printMatrix(dp)


if __name__ == "__main__":
    main()
