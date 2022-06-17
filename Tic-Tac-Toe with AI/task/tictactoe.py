# write your code here
import random


def check_start(cells):
    if len(cells) != 9:
        return False
    for i in cells:
        if i not in cell_symbols:
            return False
    return True


def print_board(board):
    print('-' * 9)
    for row in board:
        print(f'| {row[0]} {row[1]} {row[2]} |'.replace('_', ' '))
    print('-' * 9)


def check_move(board, move):

    valid_moves = '1', '2', '3'
    numbers = '1234567890'
    move_list = [i for i in move]
    # print(move_list)
    if not move_list:
        return False
    elif len(move_list) != 3:
        print('You should enter numbers!')
        return False
    elif move_list[1] != ' ':
        print('You should enter numbers!')
        return False
    elif move_list[0] not in valid_moves or move_list[2] not in valid_moves:
        if move_list[0] in numbers and move_list[2] in numbers:
            print('Coordinates should be from 1 to 3!')
            return False
        else:
            print('You should enter numbers!')
            return False
    move_y_, move_x_ = int(move_list[2]) - 1, int(move_list[0]) - 1
    # print(move_x_, move_y_)
    if board[move_x_][move_y_] != '_':
        print('This cell is occupied! Choose another one!')
        return False

    return True


def decide_next_symbol(board):
    x_count = 0
    o_count = 0
    for row in board:
        x_count += row.count('X')
        o_count += row.count('O')
    if x_count == o_count:
        return 'X'
    else:
        return 'O'


def make_board(string):
    board_list = []
    for row in [string[i:i + 3] for i in range(0, len(string), 3)]:
        row_list = []
        for i in row:
            row_list.append(i)
        board_list.append(row_list)
    return board_list


def check_win(board):
    win_combos = [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]],
                  [[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]],
                  [[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]
    empty_count = 0
    for row in board:
        empty_count += row.count('_')
    for a, b, c in win_combos:
        if board[a[0]][a[1]] == board[b[0]][b[1]] and board[a[0]][a[1]] == board[c[0]][c[1]] and \
                board[a[0]][a[1]] != '_':
            print(board[a[0]][a[1]], 'wins')
            return True

    if empty_count > 0:
        # print('Game not finished')
        return False
    elif empty_count == 0:
        print('Draw')
        return True


def robot_move(board, level='easy', pla_='X', opp_='O'):
    empty_spaces = []
    for n, i in enumerate(board):
        for z, x in enumerate(i):
            if x == '_':
                empty_spaces.append([n, z])
    if level == 'easy':
        return random.choice(empty_spaces)
    elif level == 'medium':
        win_combos = [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]],
                      [[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]],
                      [[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]
        for a, b, c in win_combos:
            x, y, z = board[a[0]][a[1]], board[b[0]][b[1]], board[c[0]][c[1]]
            if x == y and z == '_' and x != z:
                return c[0], c[1]
            elif y == z and x == '_' and x != y:
                return a[0], a[1]
            elif x == z and y == '_' and x != y:
                return b[0], b[1]
        else:
            return random.choice(empty_spaces)
    elif level == 'hard':
        return findBestMove(board, pla_, opp_)


player, opponent = 'X', 'O'


# This function returns true if there are moves
# remaining on the board. It returns false if
# there are no moves left to play.
def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if (board[i][j] == '_'):
                return True
    return False


# This is the evaluation function as discussed
# in the previous article ( http://goo.gl/sJgv68 )
def evaluate(b, pla_, opp_):
    # Checking for Rows for X or O victory.
    for row in range(3):
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
            if (b[row][0] == pla_):
                return 10
            elif (b[row][0] == opp_):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(3):

        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):

            if (b[0][col] == pla_):
                return 10
            elif (b[0][col] == opp_):
                return -10

    # Checking for Diagonals for X or O victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):

        if (b[0][0] == pla_):
            return 10
        elif (b[0][0] == opp_):
            return -10

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]):

        if (b[0][2] == pla_):
            return 10
        elif (b[0][2] == opp_):
            return -10

    # Else if none of them have won then return 0
    return 0


# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board
def minimax(board, depth, isMax, pla_, opp_):
    score = evaluate(board, pla_, opp_)

    # If Maximizer has won the game return his/her
    # evaluated score
    if (score == 10):
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if (score == -10):
        return score

    # If there are no more moves and no winner then
    # it is a tie
    if (isMovesLeft(board) == False):
        return 0

    # If this maximizer's move
    if (isMax):
        best = -1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if (board[i][j] == '_'):
                    # Make the move
                    board[i][j] = pla_

                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(board,
                                             depth + 1,
                                             not isMax, pla_, opp_))

                    # Undo the move
                    board[i][j] = '_'
        return best

    # If this minimizer's move
    else:
        best = 1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if (board[i][j] == '_'):
                    # Make the move
                    board[i][j] = opp_

                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not isMax, pla_, opp_))

                    # Undo the move
                    board[i][j] = '_'
        return best


# This will return the best possible move for the player
def findBestMove(board, pla_, opp_):
    bestVal = -1000
    bestMove = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(3):
        for j in range(3):

            # Check if cell is empty
            if (board[i][j] == '_'):

                # Make the move
                board[i][j] = pla_

                # compute evaluation function for this
                # move.
                moveVal = minimax(board, 0, False, pla_, opp_)

                # Undo the move
                board[i][j] = '_'

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if (moveVal > bestVal):
                    bestMove = (i, j)
                    bestVal = moveVal

    return bestMove







cell_symbols = 'X', 'O', '_'
starting_cells = ''


# while not check_start(starting_cells):
#     starting_cells = input('Enter the cells:')


# tic_tac_toe = make_board(starting_cells)
menu = ''
while menu != 'exit':
    menu = input('Input command:')
    if menu == 'exit':
        break
    else:
        tic_tac_toe = make_board('_' * 9)
        menu_items = menu.split()
        menu_options = 'user', 'easy', 'medium', 'hard'
        if menu_items[0] != 'start':
            print('Bad parameters!')
            continue
        elif len(menu_items) != 3:
            print('Bad parameters!')
            continue
        elif menu_items[1] not in menu_options or menu_items[2] not in menu_options:
            print('Bad parameters!')
            continue

        player_1 = menu_items[1]
        player_2 = menu_items[2]

        print_board(tic_tac_toe)
        while not check_win(tic_tac_toe):
            if player_1 == 'user':
                move = ''
                while not check_move(tic_tac_toe, move):
                    move = input('Enter the coordinates:')
                    move = move.strip()  # fix double spaces
                    move = move.replace('  ', ' ')
                move_x, move_y = int(move[0]) - 1, int(move[2]) - 1
            else:
                move_x, move_y = robot_move(tic_tac_toe, level=player_1)
                print(f'Making move level "{player_1}"')
            tic_tac_toe[move_x][move_y] = decide_next_symbol(tic_tac_toe)
            print_board(tic_tac_toe)
            if check_win(tic_tac_toe):
                break
            if player_2 == 'user':
                move = ''
                while not check_move(tic_tac_toe, move):
                    move = input('Enter the coordinates:')
                    move = move.strip()  # fix double spaces
                    move = move.replace('  ', ' ')
                move_x, move_y = int(move[0]) - 1, int(move[2]) - 1
            else:
                move_x, move_y = robot_move(tic_tac_toe, level=player_2, pla_='O', opp_='X')
                print(f'Making move level "{player_2}"')
            tic_tac_toe[move_x][move_y] = decide_next_symbol(tic_tac_toe)
            print_board(tic_tac_toe)
            if check_win(tic_tac_toe):
                break


