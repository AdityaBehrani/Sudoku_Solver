"""Used to solve 9x9 Sudoku puzzles.

All relavent functions to puzzle solving are in
the PuzzleSolver class and hte main funcion will except
singlular puzzles or a text file with multiple.
Refer to the README for more information.
"""

import sys
import time


class PuzzleSolver:
    """Class encapsulates all necessary functions to solve a 9x9 sudoku puzzle"""

    def __init__(self):
        self.n = 9
        self.length = 3
        self.width = 3
        self.cell_dependencies = self.create_cell_dependencies()

    def get_affected_cells(self, pos):
        row = pos // 9
        col = pos % 9
        subgrid_row = row // 3
        subgrid_col = col // 3

        affected_cells = set()

        # Add cells from the same row
        for i in range(9):
            affected_cells.add(row * 9 + i)

        # Add cells from the same column
        for i in range(9):
            affected_cells.add(i * 9 + col)

        # Add cells from the same 3x3 subgrid
        for i in range(3):
            for j in range(3):
                affected_cells.add((subgrid_row * 3 + i) * 9 + subgrid_col * 3 + j)

        return affected_cells

    def create_cell_dependencies(self):
        cell_dependencies = {}
        for pos in range(81):
            cell_dependencies[pos] = self.get_affected_cells(pos)
        return cell_dependencies

    def create_constraints(self, puzzle: str) -> dict[int, set]:
        """Map possible values for a given cell"""
        constraints = {}

        for cell in range(self.n**2):
            if puzzle[cell] != ".":
                continue

            constraints[cell] = (
                self.row_constraints(puzzle, cell)
                & self.col_constraints(puzzle, cell)
                & self.box_constraints(puzzle, cell)
            )
        return constraints

    def row_constraints(self, puzzle: str, cell: int) -> set:
        """Map possible values for a given cell based on row"""
        row_output = set("123456789")
        row = cell // self.n

        for offset in range(self.n):
            idx = row * self.n + offset

            if puzzle[idx] != ".":
                row_output.remove(puzzle[idx])

        return row_output

    def col_constraints(self, puzzle: str, cell: int) -> set:
        """Map possible values for a given cell based on column"""
        col_output = set("123456789")
        col = cell % self.n

        for offset in range(self.n):
            idx = col + self.n * offset

            if puzzle[idx] != ".":
                col_output.remove(puzzle[idx])

        return col_output

    def box_constraints(self, puzzle: str, cell: int) -> set:
        """Map possible values for a given cell based on box"""
        box_output = set("123456789")
        box_row = cell // (self.n * self.length)
        box_col = cell % self.n // self.width

        for x in range(self.length):
            start = (box_row * self.length + x) * self.n + box_col * self.width
            for i in range(start, start + self.width):
                if puzzle[i] != ".":
                    box_output.remove(puzzle[i])

        return box_output

    def check_sum(self, puzzle: str) -> int:
        """Sums the digits of a puzzle.

        Used as a secondary check to make sure the solution is valid
        and that the digits sum to a toal of 405
        """
        tot = 0
        for char in puzzle:
            if char != ".":
                tot += int(char)
        return tot

    def is_solved(self, puzzle: str) -> bool:
        """Checks for any remaining empty spaces in the puzzle"""
        return "." not in puzzle

    def best_choice(self, constraints: dict[int, set]) -> int:
        """Finds the most constrained cell and returns its index"""
        most_constrained_length = float("inf")
        idx = -1

        for cell in constraints:
            possible_values = len(constraints[cell])
            if most_constrained_length > possible_values:
                most_constrained_length = possible_values
                idx = cell

        return idx

    def choices(self, puzzle: str, constraints: dict[int, set]):
        """Creates potential puzzles based on current constraints"""
        output = []
        pos = self.best_choice(constraints)

        if pos == -1:
            return output

        for char in constraints[pos]:
            output.append((str(puzzle[:pos] + char + puzzle[pos + 1 :]), char, pos))

        return output

    def solve(
        self, puzzle: str, constraints: dict[int, set], empty_counter: int
    ) -> str:
        """Main function used to solve puzzles"""
        if len(constraints.keys()) < empty_counter:
            return ""

        if empty_counter == 0:
            return puzzle

        for choice, char, pos in self.choices(puzzle, constraints):
            altered = set()
            removed = set()
            original = constraints[pos]
            del constraints[pos]

            for dep_pos in self.cell_dependencies[pos]:
                if dep_pos in constraints and char in constraints[dep_pos]:
                    constraints[dep_pos].remove(char)
                    altered.add(dep_pos)
                    if len(constraints[dep_pos]) == 0:
                        removed.add(dep_pos)
                        del constraints[dep_pos]

            res = self.solve(choice, constraints, empty_counter - 1)

            if res:
                return res

            for dep_pos in removed:
                constraints[dep_pos] = set()

            for dep_pos in altered:
                constraints[dep_pos].add(char)

            constraints[pos] = original

        return ""

    def run_file(self, filename: str) -> None:
        """Tries to solve every puzzle in the provided txt file"""
        tot_start = time.time()

        puzzle_list = []
        with open(filename, "r", encoding="ascii") as file:
            puzzle_list = file.readlines()

        for idx, puzzle in enumerate(puzzle_list):
            start = time.time()
            puzzle = puzzle.strip()
            solution = self.solve(
                puzzle, self.create_constraints(puzzle), puzzle.count(".")
            )

            print(
                f"{f'Puzzle {idx + 1}':<12}: {puzzle}\n"
                + f"{'Solution':<12}: {solution}\n"
                + f"{'Time':<12}: {round((time.time() - start), ndigits=2)} seconds\n"
            )

        print(
            f"Total time to solve {len(puzzle_list)} puzzles was \
            {round(time.time() - tot_start, ndigits=2)} seconds"
        )

    def run_single_puzzle(self, puzzle: str) -> None:
        """Runs a single puzzle"""

        start = time.time()
        solution = self.solve(
            puzzle, self.create_constraints(puzzle), puzzle.count(".")
        )
        print(
            f"{'Puzzle':<12}: {puzzle}\n"
            + f"{'Solution':<12}: {solution}\n"
            + f"{'Time':<12}: {round((time.time() - start), ndigits=2)} seconds\n"
        )

    def run(self, arg: str) -> None:
        """Main runner"""

        if arg[-4:] == ".txt":
            self.run_file(arg)
        else:
            self.run_single_puzzle(arg)


if __name__ == "__main__":
    args = sys.argv[1:]
    solver = PuzzleSolver()

    if len(args) == 1:
        solver.run(args[0].strip())
    else:
        print("Incorrect arguments format.\n" + "See README for instructions.\n")
