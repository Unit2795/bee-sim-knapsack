import os

# Format and print the dynamic programming table (2D Matrix)
def printMatrix(matrix, title, reverse=False):
    matrix = matrix[::-1] if reverse else matrix

    print(title)
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))


def printInfoMessage(message):
    if os.environ.get("DEBUG"):
        print(f"INFO: {message}")