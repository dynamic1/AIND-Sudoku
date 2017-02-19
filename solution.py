from pprint import pprint
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return[s + t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_units = [['A1','B2','C3','D4','E5','F6', 'G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1'] ]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # go through all the units and find naked twins
    for unit in unitlist:
        twins_in_unit = {}
        for box in unit:
            # print(unit)
            #print("looking at unit: " + ', '.join(unit))

            if len(values[box]) == 2:
                #print("found 2 values: %s in %s" % (values[box], box))
                if values[box] not in twins_in_unit:
                    #print('insert %s' % values[box])
                    twins_in_unit[values[box]] = 1
                else:
                    #print("inc %s " %(values[box]))
                    twins_in_unit[values[box]] += 1
        #print("found twins: ")
        # pprint(twins_in_unit)

        for twin_values in twins_in_unit:
            if twins_in_unit[twin_values] != 2:
                continue
            for v in twin_values:
                for box in unit:
                    if (values[box]!=twin_values) and (v in values[box]):
                        #eliminate the value v from possibilities for box
                        assign_value(values, box, values[box].replace(v, ''))

    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """

    new_values = {}
    counter = 0
    sol = dict(values)
    for box, val in sol.items():
        if val in ['1','2','3','4','5','6','7', '8','9']:
            # print('found %s in %s' %(val, box))
            for peer in peers[box]:
                if val in sol[peer]:
                    #print("am gasit %s in %s" % (val, sol[peer]))
                    #print("%s=%s: elimin %s din %s ( %s ) -> %s" % (box, val, val, peer, sol[peer], sol[peer].replace(val, '')))
                    sol[peer] = sol[peer].replace(val, '')
                    assign_value(sol, peer, sol[peer].replace(val, ''))

    return sol

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    sol = dict(values)

    for unit in unitlist:
        # print(unit)
        for symbol in ['1','2','3','4','5','6','7', '8','9']:
            boxes_with_symbol = list(filter(lambda x: symbol in sol[x], unit))
            # print("found %s in %s" % (symbol, boxes_with_symbol))
            if len(boxes_with_symbol) == 1:
                # print("unique")
                box = boxes_with_symbol.pop()
                sol[box] = symbol
                assign_value(sol, box, symbol)
    return sol


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        values = naked_twins(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function

    new_values = reduce_puzzle(values)
    if new_values is False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved = list(filter(lambda x: len(new_values[x]) > 1, boxes))
    if len(unsolved) == 0:
        print("no more choices left to try")
        return new_values
    mybox = sorted(unsolved, key=lambda x: len(new_values[x]), reverse=True).pop()
    print("chose %s = %s" % (mybox, new_values[mybox]))
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!


    for symbol in new_values[mybox]:
        copy_values = dict(new_values)
        copy_values[mybox] = symbol
        print("trying %s = %s" % (mybox, copy_values[mybox]))
        # display(copy_values)
        possible_solution = search(copy_values)
        if possible_solution is not False:
            return possible_solution
    # If you're stuck, see the solution.py tab!
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    puzzle = grid_values(grid)
    return search(puzzle)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # display(solve(diag_sudoku_grid))



    display(solve(diag_sudoku_grid))

    #print(row_units)
    #print(diag_units)
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
