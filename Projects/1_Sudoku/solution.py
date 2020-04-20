from utils import cross, cols, rows, boxes, extract_peers, extract_units, grid2values, display, history

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units

# Update the unit list to add the new diagonal units
firstNum = 1
lastNum = 9
diagonal_unit_l = []
diagonal_unit_r = []
for num, row in enumerate(rows):
    diagonal_unit_l.append("{}{}".format(row, firstNum))
    diagonal_unit_r.append("{}{}".format(row, lastNum))
    firstNum += 1
    lastNum -= 1

unitlist = unitlist + [diagonal_unit_l] + [diagonal_unit_r]

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # copy the values
    out = values.copy()

    # get the potential pairs by iterating over each unit
    potential_pairs = []
    for unit in unitlist:
        for box in unit:
            if(len(out[box]) == 2):
                potential_pairs.append(box)

    # get the real twin pairs
    twins = []
    # iterate over each potential pair
    for p in potential_pairs:
        # and find the boxes which have peers with the same value
        for pe in peers[p]:
            if out[pe] == out[p]:
                twins.append([p, pe])

    for i in range(len(twins)):
        # get the peers of each box
        peer_elements = set(peers[twins[i][0]]) & set(peers[twins[i][1]])
        # delete the twins from each peer
        for p in peer_elements:
            if len(out[p]) > 1:
                for val in out[twins[i][0]]:
                    out[p] = out[p].replace(val, '')

    return out


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    # check if each box is solved
    if all(len(values[s]) == 1 for s in boxes):
        # check if the diagonals are solved, too
        diagonal_r = []
        diagonal_l = []

        for unit in diagonal_unit_r:
            if values[unit] not in diagonal_r:
                diagonal_r.append(values[unit])

        for unit in diagonal_unit_l:
            if values[unit] not in diagonal_l:
                diagonal_l.append(values[unit])

        if len(diagonal_l) == len(diagonal_unit_l) and len(diagonal_r) == len(diagonal_unit_r):
            return values  # Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid1 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid2 = "........4......1.....6......7....2.8...372.4.......3.7......4......5.6....4....2."
    diag_sudoku_grid3 = "9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................"
    diag_sudoku_grid4 = "2.............6.....1....7.......................................5..............."
    grids = [
        # diag_sudoku_grid1,
        # diag_sudoku_grid2,
        # diag_sudoku_grid3,
        diag_sudoku_grid4
    ]

    for grid in grids:
        print("\n")
        # display(grid2values(grid))
        result = solve(grid)
        # print("result = ", result)
        print("Done? ", result["C7"] != result["E5"])
        print("\n")
        display(result)
        print("\n")
