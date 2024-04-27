import sys
import time
args = sys.argv[1:]


# globals
global N, LENGTH, WIDTH, SYMSET
N = 9
LENGTH = 3
WIDTH = 3
SYMSET = set('123456789')


def create_constraints(puzzle: str) -> dict[int, set]:
    """ Creates a dictionary mapping the possible 
        values for a given cell to each position
    """

    constraints = {}

    for cell in range(N**2):
        if puzzle[cell] != '.':
            continue

        constraints[cell] = (row_constraints(puzzle, cell)
                           & col_constraints(puzzle, cell)
                           & box_constraints(puzzle, cell))
    return constraints


def row_constraints(puzzle: str, cell: int) -> set:
    """ Defines the possible values for a cell based on
        values in its row
    """

    row_output = set('123456789')
    row = cell // N

    for offset in range(N):
        idx = row * N + offset

        if puzzle[idx] != '.':
            row_output.remove(puzzle[idx])

    return row_output


def col_constraints(puzzle: str, cell: int) -> set:
    """ Defines the possible values for a cell based on
        values in its column
    """

    col_output = set('123456789')
    col = cell % N

    for offset in range(N):
        idx = col + N * offset

        if puzzle[idx] != '.':
            col_output.remove(puzzle[idx])

    return col_output


def box_constraints(puzzle: str, cell: int) -> set:
    """ Defines the possible values for a cell based on
        values in its box
    """

    box_output = set('123456789')
    box_row = cell // (N * LENGTH)
    box_col = cell % N // WIDTH

    for x in range(LENGTH):
        start = (box_row * LENGTH + x) * N + box_col * WIDTH
        for i in range(start, start+WIDTH):
            if puzzle[i] != '.':
                box_output.remove(puzzle[i])

    return box_output


def is_invalid(constraints: dict[int, set]) -> bool:
    """ Checks if the current set of constraints allows
        for a puzzle to be completed
    """

    for cell in constraints:
        if len(constraints[cell]) == 0:
            return True
    return False


def check_sum(puzzle: str) -> int:
    """ Sums the digits of a puzzle to make sure they sum to 405
        Used as a secondary check to make sure the solution is valid
    """

    tot = 0
    for char in puzzle:
        if char != '.':
            tot += int(char)
    return tot


def is_solved(puzzle: str) -> bool:
    """ Checks for any remaining empty spaces in the puzzle
    """

    return '.' not in puzzle


def best_choice(constraints: dict[int, set]) -> int:
    """ Finds the most constrained cell and returns its index
    """

    most_constrained_length = float('inf')
    idx = -1

    for cell in constraints:
        if most_constrained_length > len(constraints[cell]):
            most_constrained_length = len(constraints[cell])
            idx = cell

    return idx


def choices(puzzle: str, constraints: dict[int, set]) -> list[str]:
    """ Creates potential puzzles based on current constraints
        and returns a list
    """
    output = []
    pos = best_choice(constraints)

    for char in constraints[pos]:
        output.append(str(puzzle[:pos] + char + puzzle[pos+1:]))

    return output


def solve(puzzle: str, constraints: dict[int, set]) -> str:
    """ Main function used to solve puzzles
    """

    if is_invalid(constraints):
        return ""

    if is_solved(puzzle):
        return puzzle

    for choice in choices(puzzle, constraints):
        res = solve(choice, create_constraints(choice))
        if res:
            return res

    return ""


def run_file(filename: str) -> None:
    """ Tries to solve every puzzle in the provided txt file
    """
    tot_start = time.time()

    puzzle_list = []
    with open(filename, 'r', encoding="ascii") as file:
        puzzle_list = file.readlines()

    for idx, puzzle in enumerate(puzzle_list):
        start = time.time()
        puzzle = puzzle.strip()
        solution = solve(puzzle, create_constraints(puzzle))

        print(f"{f'Puzzle {idx}':<12}: {puzzle}\n"
            + f"{'Solution':<12}: {solution}\n"
            + f"{'Time':<12}: {str(time.time() - start)} seconds\n")

    print(f'Total time to solve {len(puzzle_list)} puzzles was \
          {str(time.time() - tot_start)} seconds')


def run_single_puzzle(puzzle: str) -> None:
    """ Runs a single puzzle
    """

    start = time.time()
    solution = solve(puzzle, create_constraints(puzzle))
    print(f"{'Puzzle':<10}: {puzzle}\n"
        + f"{'Solution':<10}: {solution}\n"
        + f"{'Time':<10}: {str(time.time() - start)} seconds\n")


def run(arg: str):
    """ Main runner
    """

    if arg[-4:] == '.txt':
        run_file(arg)
    else:
        run_single_puzzle(arg)


def __main__():
    if len(args) == 1:
        run(args[0].strip())
    elif len(args) == 0:
        print("Incorrect arguments format\n"
            + "See README for instructions.\n")
