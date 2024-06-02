import numpy as np
from beesim import BeeSimulator


def get_matrices():
    dp = read_matrix("matrices/dp_table.npy")
    traceback = read_matrix("matrices/traceback.npy")
    return [dp, traceback]


def read_matrix(file_path):
    return np.load(file_path, allow_pickle=True)


def save_matrix(matrix, file_path):
    # Convert the matrix to a NumPy array if it's not already one
    np_array = np.array(matrix)
    np.save(file_path, np_array)


# Store a new copy of the DP table and the traceback result if they change and we know their result is correct, so we can use them in testing.
def update_matrices():
    bee_sim = BeeSimulator(0)
    bee_sim.start()

    # Store the DP table
    save_matrix(bee_sim.dp, "matrices/dp_table.npy")

    # Store the traceback result
    save_matrix(bee_sim.collected_flowers, "matrices/traceback.npy")


if __name__ == '__main__':
    update_matrices()
