import enum
import os


# Format and print the dynamic programming table (2D Matrix)
def print_matrix(matrix, title):
    print_info_message(title)
    print_info_message('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))


# Print an informational message in cyan if the DEBUG environment variable is set
def print_info_message(message):
    if os.environ.get("DEBUG"):
        print_in_color(f"INFO: {message}", MessageColor.CYAN)


# Enum to represent the color of the message and link it to corresponding ANSI escape codes/VT Sequences
class MessageColor(enum.Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'


# Print colored messages to the console using ANSI escape codes/VT Sequences
def print_in_color(message, color):
    if not isinstance(color, MessageColor):
        raise ValueError("color must be an instance of the Color enum")
    print(f"{color.value}{message}{MessageColor.RESET.value}")
