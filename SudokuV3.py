import sys
import time
import heapq

# Gloabl Variable for length of puzzle
N = 81


def create_cell_dependencies():
    dependencies = {i:set() for i in range(N)}
    
    # row dependenceis
    for cell in range(N):
        start = cell - (cell % 9)
        
        for val in range(9):
            dependencies[start].add(cell)
            start += 1
    
    # col dependenceis
    for cell in range(N):
        start = (cell % 9)
        
        for val in range(9):
            dependencies[start].add(cell)
            
            start += 9
    
    # box dependenceis
    for cell in range(N):
        row = cell // 27
        col = (cell % 9) // 3
        
        start = (row * 27) + (col * 3)
        for val in range(3):
            dependencies[start].add(cell)
            dependencies[start + 1].add(cell)
            dependencies[start + 2].add(cell)
            
            start += 9

    # remove self dependency
    for cell in range(N):
        dependencies[cell].remove(cell)
        
    return dependencies


def create_contraints(puzzle, dependencies):
    constraints = {cell:{'1', '2', '3', '4', '5', '6', '7', '8', '9'} 
                   for cell in range(N) if puzzle[cell] == '.'}
    
    for cell in range(N):
        val = puzzle[cell]
        if val == '.': 
            continue
        else:
            for dependency in dependencies[cell]:
                if dependency in constraints and val in constraints[dependency]:
                    constraints[dependency].remove(val)
    
    # find singles
    singles = []
    
    for key in constraints:
        if len(constraints[key]) == 1:
            singles.append(key)
    
    return constraints, singles


def solve(puzzle, dependencies):
    constraints, singles = create_contraints([char for char in puzzle], dependencies)
    
    updated = False
    # apply singles
    for single in singles:
        updated = True
        puzzle[single] = constraints[single].pop()
    
    # if singles were added, recalculate constriants 
    # and propogate, else, find next best decision
    if updated:
        solve(puzzle, dependencies)
    else:
    
    return ''


def run(args):
    startTime = time.time()
    
    puzzle = str(args[0]).strip()
    dependencies = create_cell_dependencies()
    res = solve(puzzle, dependencies)
    
    endTime = time.time()
    
    print('Puzzle: ' + puzzle)
    print('Solution: ' + res + ' ' + '\n'
          + 'Time: ' + str(endTime-startTime)
          + '\n')
    

# main runner
args = ['2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3']
run(args)
