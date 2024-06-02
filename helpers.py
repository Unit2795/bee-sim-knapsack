import os

# Format and print the dynamic programming table (2D Matrix)
def printMatrix(dp):
    print("Dynamic Programming Table (2D Matrix):")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in reversed(dp)]))


def printInfoMessage(message):
    if os.environ.get("DEBUG"):
        print(f"INFO: {message}")