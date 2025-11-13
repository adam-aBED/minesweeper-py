import random

def init_board(nb_rows,nb_cols,value):
    """
    int, int, any value -> list[list]
    Returns a 2D list (list of lists) with 'nb_rows' rows and 'nb_cols' columns,
    where each cell is the 'value' picked.
   
     >>> init_board(2, 3, 'X')
    [['X', 'X', 'X'], ['X', 'X', 'X']]
    >>> init_board(3, 2, 0)
    [[0, 0], [0, 0], [0, 0]]
    >>> init_board(1, 4, None)
    [[None, None, None, None]]
    """
    
    board = []
    for i in range(nb_rows):
        row = []
        for j in range(nb_cols):
            row.append(value)
        board.append(row)
    return board


def count_total(board, value):
    """
    (list[list], any value) -> int
    Returns the total number of occurrences of 'value' in the 2D list 'board'.

    >>> count_total([['X', 'O', 'X'], ['O', 'X', 'O']], 'X')
    3
    >>> count_total([[1, 2, 3], [4, 5, 1], [1, 6, 7]], 1)
    3
    >>> count_total([['A', 'B'], ['C', 'D']], 'E')
    0
    """

    counter = 0
    for row in board:
        for cell in row:
            if cell == value:
                counter += 1
    return counter


def is_valid_position(board, position_row, position_col):
    """
    (list[list], int, int) -> bool
    Returns True if the position (row, col) is valid within the 2D list 'board',
    otherwise returns False.

    >>> is_valid_position([['X', 'O'], ['O', 'X']], 1, 1)
    True
    >>> is_valid_position([[1, 2, 3], [4, 5, 6]], 2, 0)
    False
    >>> is_valid_position([['A', 'B'], ['C', 'D']], 0, 2)
    False
    """

    # handle empty board or empty first row
    if not board or not board[0]:
        return False
    
    min_position = 0
    nb_rows = len(board) - 1
    nb_cols = len(board[0]) - 1

    if position_row < min_position or position_col < 0:
        return False
    
    if position_row > nb_rows or position_col > nb_cols:
        return False
    
    return True


def get_neighbour_positions(board, position_row, position_col):
    """
    (list[list], int, int) -> list[[int, int]]
    Returns a list of valid neighboring positions (row, col) for the given position
    in the 2D list 'board'. Neighbors are the cells directly adjacent horizontally,
    vertically, and diagonally.

    >>> get_neighbour_position([['X', 'O', 'X'], ['O', 'X', 'O'], ['X', 'O', 'X']], 1, 1)
    [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    >>> get_neighbour_position([[1, 2], [3, 4]], 0, 0)
    [[0, 1], [1, 0], [1, 1]]
    >>> get_neighbour_position([['A', 'B', 'C'], ['D', 'E', 'G']], 1, 2)
    [[0, 1], [0, 2], [1, 1]]
    """

    neighbours = []
    # Loop through all possible row and columns diagonal, horizontal, vertical (-1, 0, 1)
    for change_row in [-1, 0, 1]:
        for change_col in [-1, 0, 1]:
            
            # Skip the current cell itself (0, 0)
            if not (change_row == 0 and change_col == 0):
                
                new_row = position_row + change_row
                new_col = position_col + change_col
                
                if is_valid_position(board, new_row, new_col):
                    neighbours.append([new_row, new_col])
                    
    return neighbours


def count_neighbours(board, position_row, position_col, value):
    """
    (list[list], int, int, any value) -> int
    Returns the count of neighboring cells that contain the specified 'value'
    around the given position in the 2D list 'board'.
    >>> count_neighbours([['X', 'O', 'X'], ['O', 'X', 'O'], ['X', 'O', 'X']], 1, 1, 'X')
    4
    >>> count_neighbours([[1, 2, 3], [4, 1, 6], [7, 8, 1]], 1, 1, 1)
    2
    >>> count_neighbours([['A', 'B'], ['C', 'D']], 0, 0, 'E')
    0
    """
    neighbours = get_neighbour_positions(board, position_row, position_col)
    counter = 0
    
    for neighbour in neighbours:
        row, col = neighbour
        if board[row][col] == value:
            counter += 1
            
    return counter


def new_mine_position(board):
    """
    list[list[list]] -> int, int
    Returns a random position (row, col) on the 2D list 'board' that does
    contain a mine (represented by -1).

    >>> random.seed(202)
    >>> new_mine_position([[0, -1, 0], [0, 0, 0], [-1, 0, 0]])
    (1, 2)  # Example output of an output bc it is random
    >>> new_mine_position([[0, 0], [0, 0]])
    (0, 1)  
    >>> new_mine_position([[-1, 0, 0], [0, -1, 0], [0, 0, 0]])
    (2, 2)  
    """

    nb_rows = len(board)
    nb_cols = len(board[0])

    while True:
        row = random.randint(0, nb_rows - 1)
        col = random.randint(0, nb_cols - 1)

        if board[row][col] != -1:
            return (row, col)


def new_mine(board):
    """
    list[list[list]] -> None
    Places a mine (represented by -1) at a random position on the 2D list 'board'
    that does not already contain a mine. Places value 1 around the mine.
    >>> board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    new_mine(board)
    # board could now be: [[1, 1, 1], [1, -1, 1], [1, 1, 1]]  # Example output
    >>> board = [[0, 0], [0, 0]]
    new_mine(board)
    # board could now be: [[1, 1], [1, -1]]
    """

    row, col = new_mine_position(board)
    board[row][col] = -1
    
    for change_row in [-1, 0, 1]:
        for change_col in [-1, 0, 1]:
            
            # Skip the current cell itself (0, 0)
            if not (change_row == 0 and change_col == 0):
                
                new_row = row + change_row
                new_col = col + change_col
                
                if is_valid_position(board, new_row, new_col):
                    if board[new_row][new_col] != -1:
                        board[new_row][new_col] += 1


def generate_helper_board(nb_rows, nb_cols, nb_mines):
    """
    int, int, int -> list[list]
    Generates a helper board for Minesweeper with the specified number of rows,
    columns, and mines. The board contains -1 for mines and numbers indicating
    the count of adjacent mines.

    >>> generate_helper_board(3, 3, 1)
    # Example output: [[0, 1, 0], [1, -1, 1], [0, 1, 0]]
    >>> generate_helper_board(2, 2, 2)
    # Example output: [[-1, -1], [2, 2]]
    """

    board = init_board(nb_rows, nb_cols, 0)
    
    for _ in range(nb_mines):
        new_mine(board)
        
    return board


def flag(board, row, col):
    """
    (list[list], int, int) -> None
    Flags the cell at the specified position (row, col) on the board by setting
    its value to '\u2691'. If the cell is already flagged, it unflags it by setting 
    it back to '?'.

    >>> board = [['X', 'O'], ['O', 'X']]
    flag(board, 0, 1)
    # board is now [['X', '\u2691'], ['O', 'X']]
    >>> flag(board, 0, 1)
    # board is now [['X', '?'], ['O', 'X']]
    """

    if board[row][col] == '?':
        board[row][col] = '\u2691'
    
    elif board[row][col] == '\u2691':
        board[row][col] = '?'
    

def reveal(helper_board, game_board, row, col):
    """
    (list[list], list[list], int, int) -> None
    Reveals the cell at the specified position (row, col) on the game board
    based on the helper board. If the cell contains a mine (-1), raises an
    AssertionError indicating the player has lost. Otherwise, updates the game
    board with the value from the helper board.
    >>> helper_board = [[0, 1, -1], [1, 2, 1], [0, 1, 0]]
    game_board = [['?', '?', '?'], ['?', '?', '?'], ['?', '?', '?']]
    reveal(helper_board, game_board, 0, 0)
    # game_board is now [['0', '?', '?'], ['?', '?', '?'], ['?', '?', '?']]
    >>> reveal(helper_board, game_board, 0, 2)
    # Raises AssertionError: "BOOM! You lost."
    """

    value = helper_board[row][col]

    if value == -1:
        raise AssertionError("BOOM! You lost.")
    
    game_board[row][col] = str(value)


def print_board(board):
    """
    (list[list]) -> None
    Prints the 2D list 'board' in a formatted manner for better visualization.

    >>> print_board([['X', 'O'], ['O', 'X']])
    X O
    O X
    """

    for row in board:
        print(' '.join(row))


def play():
    """
    () -> None
    Starts an interactive Minesweeper game in the console.

    The user first chooses how many rows and columns they want for the board,
    as well as a difficulty level (EASY, MEDIUM, or HARD). The difficulty
    determines how many mines will be randomly placed.

    During the game, the current board and the number of mines remaining are
    displayed each turn. Choices made by user:
      - 0 to reveal a cell, or
      - 1 to flag a cell that is possibly mine.

    Revealing a cell that contains a mine will raise
    AssertionError('BOOM! You lost.'). If the player manages to reveal all
    safe cells, all remaining unknown cells ('?') are replaced with flags,
    and a congratulatory message is shown WITH THE FINAL WORD.
    """
    nb_rows = int(input("Enter number of rows for the board: "))
    nb_cols = int(input("Enter number of columns for the board: "))
    difficulty = input("Choose a difficulty from [EASY, MEDIUM, HARD]: ")

    total_cells = nb_rows * nb_cols

    if difficulty == "EASY":
        nb_mines = int(0.10 * total_cells)
    elif difficulty == "MEDIUM":
        nb_mines = int(0.30 * total_cells)
    else:
        nb_mines = int(0.50 * total_cells)

    helper_board = generate_helper_board(nb_rows, nb_cols, nb_mines)
    game_board = init_board(nb_rows, nb_cols, "?")

    target_revealed = total_cells - nb_mines
    revealed = total_cells - count_total(game_board, '?') - count_total(game_board, '\u2691')
   
    while revealed < target_revealed:
        mines_remaining = nb_mines - count_total(game_board, '\u2691')
        print("Current Board: (" + str(mines_remaining) + " mines remaining)")
        print_board(game_board)

        action = int(input("Choose 0 to reveal or 1 to flag "))
        row = int(input("Which row? "))
        col = int(input("Which column? "))

        if action == 0:
            reveal(helper_board, game_board, row, col)
        elif action == 1:
            flag(game_board, row, col)

        
        revealed = total_cells - count_total(game_board, '?') - count_total(game_board, '\u2691')
    # Game won: flag all remaining '?' cells
    for i in range(nb_rows):
        for j in range(nb_cols):
            if game_board[i][j] == '?':
                game_board[i][j] = '\u2691'

    print("Congratulations! You won!\nFinal Board:")
    print_board(game_board)

def solve_cell(board, row, col, left_click, right_click):
    """
    (list[list[str]], int, int, (int,int), (int,int)) -> None
    Applies Minesweeper solving rules to the cell at (row, col) on the board.
    Uses left_click to reveal cells and right_click to flag cells.
    """
    cell = board[row][col]

    if cell == '?' or cell == '\u2691':
        return

    number_adjacent_mines = int(cell)

    # Neighbour coordinates (reuse your helper; you named it get_neighbour_position)
    neighbours = get_neighbour_positions(board, row, col)

    # Count neighbour categories
    flagged = 0
    unknown = 0
    total_neigh = 0
    i = 0
    while i < len(neighbours):
        nr, nc = neighbours[i][0], neighbours[i][1]
        val = board[nr][nc]
        if val == '\u2691':
            flagged = flagged + 1
        elif val == '?':
            unknown = unknown + 1
        # else: revealed number (string)
        total_neigh = total_neigh + 1
        i = i + 1

    revealed_neighbours = total_neigh - flagged - unknown
    non_mines_adjacent = total_neigh - number_adjacent_mines

    # if all mines around are already flagged -> reveal all unknowns
    if flagged == number_adjacent_mines:
        j = 0
        while j < len(neighbours):
            nr, nc = neighbours[j][0], neighbours[j][1]
            if board[nr][nc] == '?':
                left_click(nr, nc)
            j = j + 1

    # if all safe neighbours are already revealed -> flag remaining unknowns
    if revealed_neighbours == non_mines_adjacent and unknown > 0:
        k = 0
        while k < len(neighbours):
            nr, nc = neighbours[k][0], neighbours[k][1]
            if board[nr][nc] == '?':
                right_click(nr, nc)
            k = k + 1


def solve(board, left_click, right_click):
    """
    (list[list[str]], (int,int), (int,int)) -> None
    Repeatedly calls solve_cell on every cell until no '?' remain.
    """

    # keep looping until there are no '?' left
    done = False
    while not done:
        done = True  # assume solved unless we find a '?'
        r = 0
        while r < len(board):
            c = 0
            while c < len(board[0]):
                if board[r][c] == '?':
                    done = False  # found an unknown → keep looping later
                solve_cell(board, r, c, left_click, right_click)
                c = c + 1
            r = r + 1