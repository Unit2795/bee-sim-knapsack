from flowers import Flower, flowers as avail_flowers
from helpers import printMatrix, printInfoMessage


def bee_simulator(flowers, flower_index, bee_energy, dp, total_flowers, choices):
    # BASE CASE: The bee has no more energy (columns) or there are no more flowers to visit (rows).
    # If you were writing the DP table by hand, this would be the first row and column.
    if bee_energy <= 0 or flower_index < total_flowers:
        return 0

    # If the current cell in the DP table has already been calculated (memoized), return the value.
    if dp[flower_index][bee_energy] != 0:
        return dp[flower_index][bee_energy]

    # Select the current flower we will be evaluating
    current_flower = flowers[flower_index]

    print(f"Considering {current_flower.type} (Row: {flower_index}, Column: {bee_energy})");

    # If the current flower's energy cost is greater than the bee's remaining energy,
    # we skip this flower and move on to the next.
    if current_flower.energy_cost > bee_energy:
        printInfoMessage(f"Skipping {current_flower.type} due to high energy cost. Needed Energy: {current_flower.energy_cost}. Available energy: {bee_energy}. Deficit: {bee_energy - current_flower.energy_cost}  (Row: {flower_index}, Column: {bee_energy})")
        return bee_simulator(flowers, flower_index + 1, bee_energy, dp, total_flowers, choices)
    else:
        # Perform a comparison between two scenarios:
        # 1. The bee collects the nectar and pollen from the current flower
        # 2. The bee skips the current flower and moves on to the next one
        # The optimal solution is the maximum nectar value of these two scenarios.
        collect = current_flower.nectar + bee_simulator(flowers, flower_index + 1,
                                                        bee_energy - current_flower.energy_cost, dp, total_flowers, choices)
        not_collect = bee_simulator(flowers, flower_index + 1, bee_energy, dp, total_flowers, choices)

        # Determine which scenario yields the maximum nectar value
        # We'll also keep track of the decision made for each flower in the choices table,
        #   so that we can backtrack later and determine what flowers were actually chosen
        if collect > not_collect:
            choices[flower_index][bee_energy] = True
            result = collect
            decision = "COLLECT"
        else:
            choices[flower_index][bee_energy] = False
            result = not_collect
            decision = "SKIP"

        # Store the result in the DP table for future reference
        dp[flower_index][bee_energy] = result

        # Print information about the current flower and the decision-making process
        printInfoMessage(f"""
        Considering {current_flower.type} (Row: {flower_index}, Column: {bee_energy})
            {current_flower.nectar} (+{current_flower.nectar} nectar), {current_flower.energy_cost} (-{current_flower.energy_cost} energy), 
            New total nectar if collected: {collect}
            New total nectar if SKIPPED: {not_collect}
            {result} (MAX of {collect} and {not_collect})
            Decision: {decision}
        """)

        return result


# Trace back the choices made to determine which flowers were actually collected by the bee
def print_collected_flowers(flowers, bee_energy, choices):
    # Start the bee with no collected flowers and maximum energy
    collected_flowers = []
    e = bee_energy

    for i in range(len(flowers)):
        if choices[i][e]:
            collected_flowers.append((flowers[i].type, flowers[i].nectar, flowers[i].energy_cost))
            e -= flowers[i].energy_cost
    for flower in collected_flowers:
        print(f"Bee collected {flower[1]} nectar from a {flower[0]}, expending {flower[2]} energy")


# Initialize parameters for the bee simulator and call the function
def main():
    # Bee energy is akin to the weight limit of the knapsack problem
    bee_energy = 10

    total_flowers = len(avail_flowers)
    # Initialize the dynamic programming table used for memoization
    # Columns represent the bee's energy and the rows represent the flowers
    dp = [[0] * (bee_energy + 1) for _ in range(total_flowers)]

    # Initialize the choices table to keep track of the flowers the bee chooses
    choices = [[False] * (bee_energy + 1) for _ in range(total_flowers)]

    reversed_flowers = avail_flowers[::-1]

    # Call the bee simulator function to find the optimal solution
    result = bee_simulator(reversed_flowers, 0, bee_energy, dp, total_flowers, choices)

    printMatrix(dp, "Dynamic Programming Table (2D Matrix)", True)
    printMatrix(choices, "Choices Table (2D Matrix)")
    print(f"Maximum nectar collected by the bee: {result}")
    print_collected_flowers(avail_flowers, bee_energy, choices)


if __name__ == "__main__":
    main()
