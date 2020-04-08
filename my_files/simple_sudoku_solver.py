rows = "ABCDEFGHI"
cols = "123456789"
grid = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."


def cross(a, b):
    return [s+t for s in a for t in b]


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

# create the column / row pairs
colRows = {}
counter = 0

for row in rows:
    for col in cols:
        tmpValue = "{}{}".format(row, col)
        gridValue = grid[counter]
        if gridValue == ".":
            gridValue = cols
        colRows.update({tmpValue: gridValue})
        counter = counter + 1


def eliminate(values):
    solved_boxes = []
    for box in values.keys():
        if(len(values[box]) == 1):
            solved_boxes.append(box)
    for solvedBox in solved_boxes:
        for peer in peers[solvedBox]:
            values[peer] = values[peer].replace(values[solvedBox], '')

    return values


def only_choice(values):
    # iterate over each box in unit, e.g. "A1" in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
    for unit in unitlist:
        for box in unit:
            possibleValues = values[box]
            # iterate again over each element in unit and compare the values
            for b in unit:
                if b != box:  # skip the current box
                    for e in values[b]:
                        possibleValues = possibleValues.replace(e, "")
            # if there is only one value left it is the only choice for this box
            if len(possibleValues) == 1:
                values[box] = possibleValues[0]
    return values


values = {'H4': '2', 'G2': '123456789', 'E2': '123456789', 'D4': '123456789', 'D6': '123456789', 'B8': '123456789', 'I9': '123456789', 'A2': '123456789', 'B7': '123456789', 'D2': '2', 'B5': '123456789', 'E6': '123456789', 'D7': '123456789', 'B3': '123456789', 'B1': '123456789', 'F4': '123456789', 'F3': '123456789', 'C7': '123456789', 'A1': '4', 'C3': '123456789', 'H7': '123456789', 'G1': '123456789', 'F1': '123456789', 'E5': '8', 'I3': '4', 'G8': '7', 'B9': '123456789', 'H3': '123456789', 'I2': '123456789', 'E8': '123456789', 'F2': '123456789', 'C2': '123456789', 'C6': '123456789', 'A9': '5', 'A5': '123456789', 'E3': '123456789', 'F6': '123456789', 'E7': '4', 'H6': '123456789', 'A6': '123456789',
          'I1': '1', 'G3': '123456789', 'F9': '123456789', 'H9': '123456789', 'D1': '123456789', 'A3': '123456789', 'D8': '6', 'H2': '123456789', 'B6': '123456789', 'B2': '3', 'B4': '123456789', 'F5': '1', 'I6': '123456789', 'E4': '123456789', 'I4': '123456789', 'G5': '123456789', 'F8': '123456789', 'C1': '123456789', 'D9': '123456789', 'D5': '123456789', 'G9': '123456789', 'G6': '3', 'E9': '123456789', 'I8': '123456789', 'H5': '123456789', 'H8': '123456789', 'H1': '5', 'C9': '123456789', 'D3': '123456789', 'C4': '7', 'G7': '123456789', 'A4': '123456789', 'G4': '6', 'A7': '8', 'I5': '123456789', 'A8': '123456789', 'C8': '123456789', 'E1': '123456789', 'F7': '123456789', 'I7': '123456789', 'C5': '123456789'}
{'H4': '2', 'G2': '123456789', 'E2': '123456789', 'D4': '123456789', 'D6': '123456789', 'B8': '123456789', 'I9': '123456789', 'A2': '123456789', 'B7': '123456789', 'D2': '2', 'B5': '123456789', 'E6': '123456789', 'D7': '123456789', 'B3': '123456789', 'B1': '123456789', 'F4': '123456789', 'F3': '123456789', 'C7': '123456789', 'A1': '4', 'C3': '123456789', 'H7': '123456789', 'G1': '123456789', 'F1': '123456789', 'E5': '8', 'I3': '4', 'G8': '7', 'B9': '123456789', 'H3': '123456789', 'I2': '123456789', 'E8': '123456789', 'F2': '123456789', 'C2': '123456789', 'C6': '123456789', 'A9': '5', 'A5': '123456789', 'E3': '123456789', 'F6': '123456789', 'E7': '4', 'H6': '123456789', 'A6': '123456789', 'I1': '1',
    'G3': '123456789', 'F9': '123456789', 'H9': '123456789', 'D1': '123456789', 'A3': '123456789', 'D8': '6', 'H2': '123456789', 'B6': '123456789', 'B2': '3', 'B4': '123456789', 'F5': '1', 'I6': '123456789', 'E4': '123456789', 'I4': '123456789', 'G5': '123456789', 'F8': '123456789', 'C1': '123456789', 'D9': '123456789', 'D5': '123456789', 'G9': '123456789', 'G6': '3', 'E9': '123456789', 'I8': '123456789', 'H5': '123456789', 'H8': '123456789', 'H1': '5', 'C9': '123456789', 'D3': '123456789', 'C4': '7', 'G7': '123456789', 'A4': '123456789', 'G4': '6', 'A7': '8', 'I5': '123456789', 'A8': '123456789', 'C8': '123456789', 'E1': '123456789', 'F7': '123456789', 'I7': '123456789', 'C5': '123456789'}


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
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
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    s = False
    for box in boxes:
        if len(values[box]) > 1:
            s = box
            break

    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


display(search(values))
