from flowers import Flower, flowers as avail_flowers


def bee_simulator(flowers, bee_energy, index, memo):
    n = len(flowers)

    if bee_energy < 0 or index >= n:
        return 0

    if memo[index][bee_energy] is not None:
        return memo[index][bee_energy]

    current_flower = flowers[index]

    if current_flower.energy_cost > bee_energy:
        result = bee_simulator(flowers, bee_energy, index + 1, memo)
    else:
        not_take = bee_simulator(flowers, bee_energy, index + 1, memo)
        take = current_flower.nectar + bee_simulator(flowers, bee_energy - current_flower.energy_cost, index + 1, memo)

        if take > not_take:
            print(f"Bee visited a {current_flower.type} flower with {current_flower.nectar} nectar. (Index: {index})")
            result = take
        else:
            result = not_take

    memo[index][bee_energy] = result
    return result


def main():
    n = len(avail_flowers)
    init_index = 0
    init_bee_energy = 100
    init_memo = [[None] * 101 for _ in range(n)]
    result = bee_simulator(avail_flowers, init_bee_energy, init_index, init_memo)
    print(f"The maximum nectar the bee can collect is {result}")


if __name__ == "__main__":
    main()
