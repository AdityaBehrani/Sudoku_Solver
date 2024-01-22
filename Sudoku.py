import sys; args = sys.argv[1:]
import time


# globals
global N, LENGTH, WIDTH, SYMSET
N = 9
LENGTH = 3
WIDTH = 3
SYMSET = set({'1', '2', '3', '4', '5', '6', '7', '8', '9'})


def create_constraints(puzzle):
    constraints = {}
    
    for cell in range(N**2):
        if puzzle[cell] != '.':
            continue
        
        constraints[cell] = (row_constraints(puzzle, cell)
                        & col_constraints(puzzle, cell)
                        & box_constraints(puzzle, cell))
    return constraints


def row_constraints(puzzle, cell):
    row_output = set({'1', '2', '3', '4', '5', '6', '7', '8', '9'})
    row = cell // N
    
    for offset in range(N):
        idx = row * N + offset
        
        if puzzle[idx] != '.':
            row_output.remove(puzzle[idx])
        
    return row_output


def col_constraints(puzzle, cell):
    col_output = set({'1', '2', '3', '4', '5', '6', '7', '8', '9'})
    col = cell % N
    
    for offset in range(N):
        idx = col + N * offset
        
        if puzzle[idx] != '.':
            col_output.remove(puzzle[idx])

    return col_output


def box_constraints(puzzle, cell):
    box_output = set({'1', '2', '3', '4', '5', '6', '7', '8', '9'})
    boxRow = cell // (N * LENGTH)
    boxCol = cell % N // WIDTH

    for x in range(LENGTH):
        start = (boxRow * LENGTH + x)* N + boxCol * WIDTH
        for i in range(start, start+WIDTH):
            if puzzle[i] != '.':
                box_output.remove(puzzle[i])
            
    return box_output


def is_invalid(constraints):
    for cell in constraints:
        if len(constraints[cell]) == 0:
            return True
    return False


def check_sum(puzzle):
    sum = 0
    for char in puzzle:
        if char != '.':
            sum += int(char)
    return sum


def is_solved(puzzle):
    return '.' not in puzzle


def best_choice(constraints):
    best = float('inf')
    idx = -1
    
    for cell in constraints:
        if best > len(constraints[cell]):
            best = len(constraints[cell])
            idx = cell
            
    return idx


def choices(puzzle, constraints):
    output = []
    pos = best_choice(constraints)
    
    for char in constraints[pos]:
        output.append(str(puzzle[:pos] + char + puzzle[pos+1:]))
        
    return output
    
    
def solve(puzzle, constraints):
    if is_invalid(constraints): return ""
    if is_solved(puzzle): return puzzle
    
    for choice in choices(puzzle, constraints):
        res = solve(choice, create_constraints(choice))
        if res: return res
    


def run_file(filename):
    tot_start = time.time()
    
    file = open(filename, 'r')
    puzzle_list = file.readlines()
    
    for idx, puzzle in enumerate(puzzle_list):
        start = time.time()
        puzzle = puzzle.strip()
        solution = solve(puzzle, create_constraints(puzzle))

        print(f"{f'Puzzle {idx}':<10}: {puzzle}\n"
            + f"{'Solution':<10}: {solution}\n"
            + f"{'Time':<10}: {str(time.time()-start)}\n")

    print(f'Total time to solve {len(puzzle_list)} puzzles was {str(time.time()-tot_start)}')


def run_single_puzzle(puzzle):
    start = time.time()
    solution = solve(puzzle, create_constraints(puzzle))
    print(f"{'Puzzle':<10}: {puzzle}\n"
        + f"{'Solution':<10}: {solution}\n"
        + f"{'Time':<10}: {str(time.time()-start)}\n")


def run(arg):
    if arg[-4:] == '.txt':
        run_file(arg)
    else:    
        run_single_puzzle(arg)
    

run(args[0].strip())