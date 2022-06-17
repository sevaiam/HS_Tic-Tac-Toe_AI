from copy import copy

from hstest import StageTest, dynamic_test, TestedProgram, CheckResult

from util.enum import GameState, CellState
from util.grid import Grid
from util.minimax import Minimax


class Test:
    def __init__(self, inp, result, state, additional_contains=None):
        self.inp = inp
        self.result = result
        self.state = state
        self.additional_contains = additional_contains


class TicTacToeTests(StageTest):
    easy_ai_moves = [0 for _ in range(9)]

    @dynamic_test(order=1)
    def test_bad_parameters(self):
        program = TestedProgram()
        program.start()

        output = program.execute("start")

        if "bad parameters" not in output.lower():
            return CheckResult.wrong("After entering start command with wrong parameters you should print "
                                     "'Bad parameters!' and ask to enter a command again!")

        output = program.execute("start easy")

        if "bad parameters" not in output.lower():
            return CheckResult.wrong("After entering start command with wrong parameters you should print "
                                     "'Bad parameters!' and ask to enter a command again!")

        program.execute("exit")

        if not program.is_finished():
            return CheckResult.wrong("After entering 'exit' command you should stop the program!")

        return CheckResult.correct()

    @dynamic_test(order=2)
    def test_grid_output(self):
        program = TestedProgram()
        program.start()

        output = program.execute("start user easy")

        printed_grid = Grid.from_output(output)
        empty_grid = Grid.from_line("_________")

        if printed_grid != empty_grid:
            return CheckResult.wrong(f"After starting the program you should print an empty grid!\n"
                                     f"Correct empty grid:\n{empty_grid}")

        if "enter the coordinates:" not in output.lower():
            return CheckResult.wrong("After printing an empty grid you should ask to enter cell coordinates!")

        output = program.execute("2 2")

        grid_after_move = Grid.from_output(output)
        correct_grid_after_move = Grid.from_line("____X____")

        if grid_after_move != correct_grid_after_move:
            return CheckResult.wrong(f"After making the move wrong grid was printed.\n"
                                     f"Your grid:\n{grid_after_move}\n"
                                     f"Correct grid:\n{correct_grid_after_move}")

        if "making move level \"easy\"" not in output.lower().replace("'", "\""):
            return CheckResult.wrong("After entering a cell coordinates you should print:\n"
                                     "Making move level \"easy\"")

        grid_after_ai_move = Grid.from_output(output, 2)

        if grid_after_ai_move == grid_after_move:
            return CheckResult.wrong("After AI move grid wasn't changed!")

        game_grid = grid_after_ai_move

        while True:
            game_state = game_grid.get_game_state()
            if game_grid.get_game_state() != GameState.NOT_FINISHED:
                if game_state == GameState.X_WIN and "X wins" not in output:
                    return CheckResult.wrong("You should print 'X wins' if X win the game!")
                if game_state == GameState.O_WIN and "O wins" not in output:
                    return CheckResult.wrong("You should print 'O wins' if O win the game!")
                if game_state == GameState.DRAW and "Draw" not in output:
                    return CheckResult.wrong("You should print 'Draw' if the game ends with draw!")
                break

            next_move = Minimax.get_move(game_grid, CellState.X)
            temp_grid = copy(game_grid)

            temp_grid.set_cell(next_move.x, next_move.y, CellState.X)

            output = program.execute(f"{next_move.x + 1} {next_move.y + 1}")

            game_grid = Grid.from_output(output)

            if game_grid != temp_grid:
                return CheckResult.wrong(f"After making move ({next_move}) the grid is wrong!\n"
                                         f"Your grid:\n{game_grid}\n"
                                         f"Correct grid:\n{temp_grid}")

            if game_grid.get_game_state() != GameState.NOT_FINISHED:
                continue

            game_grid = Grid.from_output(output, 2)

        return CheckResult.correct()

    @dynamic_test(repeat=100, order=3)
    def check_easy_ai(self):

        program = TestedProgram()
        program.start()

        program.execute("start user easy")

        output = program.execute("2 2")

        grid_after_ai_move = Grid.from_output(output, 2)

        cells = grid_after_ai_move.get_grid()

        for i in range(9):
            if i == 4:
                continue

            if cells[int(i / 3)][i % 3] == CellState.O:
                self.easy_ai_moves[i] += 1

        return CheckResult.correct()

    @dynamic_test(order=4)
    def check_random(self):

        average_score = 0

        for i in range(len(self.easy_ai_moves)):
            average_score += (i + 1) * self.easy_ai_moves[i]

        average_score /= 8

        expected_value = (1 + 2 + 3 + 4 + 6 + 7 + 8 + 9) * 100 / 8 / 8

        if abs(average_score - expected_value) > 20:
            return CheckResult.wrong("Looks like your Easy level AI doesn't make a random move!")

        return CheckResult.correct()

    is_easy_not_moving_like_medium = False

    @dynamic_test(repeat=30, order=5)
    def check_easy_not_moving_like_medium(self):

        if self.is_easy_not_moving_like_medium:
            return CheckResult.correct()

        program = TestedProgram()
        program.start()

        program.execute("start user easy")

        output = program.execute("2 2")

        game_grid = Grid.from_output(output, 2)

        cells = game_grid.get_grid()

        if cells[0][0] == CellState.EMPTY and cells[2][2] == CellState.EMPTY:
            output = program.execute("1 1")
            game_grid = Grid.from_output(output, 2)
            if game_grid.get_grid()[2][2] == CellState.EMPTY:
                self.is_easy_not_moving_like_medium = True
        else:
            output = program.execute("1 3")
            game_grid = Grid.from_output(output, 2)
            if game_grid.get_grid()[2][0] == CellState.EMPTY:
                self.is_easy_not_moving_like_medium = True

        program.stop()

        return CheckResult.correct()

    @dynamic_test(order=6)
    def check_easy_not_moving_like_medium_after(self):
        if not self.is_easy_not_moving_like_medium:
            return CheckResult.wrong("Looks like your Easy level AI doesn't make a random move!")
        return CheckResult.correct()

    @dynamic_test(order=7)
    def check_easy_vs_easy(self):

        program = TestedProgram()
        program.start()

        output = program.execute("start easy easy")

        grids = Grid.all_grids_from_output(output)

        Grid.check_grid_sequence(grids)

        return CheckResult.correct()

    @dynamic_test(repeat=10, order=8)
    def check_medium_ai(self):

        program = TestedProgram()
        program.start()
        program.execute("start user medium")

        output = program.execute("2 2")

        game_grid = Grid.from_output(output, 2)

        cells = game_grid.get_grid()

        if cells[0][0] == CellState.EMPTY and cells[2][2] == CellState.EMPTY:
            output = program.execute("1 1")
            game_grid = Grid.from_output(output, 2)
            if game_grid.get_grid()[2][2] == CellState.EMPTY:
                return CheckResult.wrong("Looks like your Medium level AI doesn't make a correct move!")
        else:
            output = program.execute("1 3")
            game_grid = Grid.from_output(output, 2)
            if game_grid.get_grid()[2][0] == CellState.EMPTY:
                return CheckResult.wrong("Looks like your Medium level AI doesn't make a correct move!")

        program.stop()

        return CheckResult.correct()

    @dynamic_test(order=9)
    def check_medium_vs_medium(self):

        program = TestedProgram()
        program.start()

        output = program.execute("start medium medium")

        grids = Grid.all_grids_from_output(output)

        Grid.check_grid_sequence(grids)

        return CheckResult.correct()

    is_medium_not_moving_like_hard = False

    @dynamic_test(repeat=30, order=10)
    def check_medium_not_moving_like_hard(self):

        if self.is_medium_not_moving_like_hard:
            return CheckResult.correct()

        program = TestedProgram()
        program.start()

        program.execute("start user medium")

        output = program.execute("2 2")

        user_move_grid = Grid.from_output(output, 1)
        medium_move_grid = Grid.from_output(output, 2)

        medium_move = Grid.get_move(user_move_grid, medium_move_grid)

        minimax_correct_positions = Minimax.get_available_positions(user_move_grid, CellState.O)

        if medium_move not in minimax_correct_positions:
            self.is_medium_not_moving_like_hard = True

        return CheckResult.correct()

    @dynamic_test(order=11)
    def check_medium_not_moving_like_hard_after(self):
        if not self.is_medium_not_moving_like_hard:
            return CheckResult.wrong("Looks like Medium level AI doesn't make a random move!")
        return CheckResult.correct()

    @dynamic_test(order=12)
    def check_hard_ai(self):

        program = TestedProgram()
        program.start()

        output = program.execute("start user hard")

        grid = Grid.from_output(output)

        next_move = Minimax.get_move(grid, CellState.X)

        output = program.execute(f"{next_move.x + 1} {next_move.y + 1}")

        while "win" not in output.lower() and "draw" not in output.lower():
            grid_after_user_move = Grid.from_output(output)
            grid_after_ai_move = Grid.from_output(output, 2)

            ai_move = Grid.get_move(grid_after_user_move, grid_after_ai_move)

            correct_minimax_positions = Minimax.get_available_positions(grid_after_user_move, CellState.O)

            if ai_move not in correct_minimax_positions:
                return CheckResult.wrong("Your minimax algorithm is wrong! It chooses wrong positions to make a move!")

            next_move = Minimax.get_move(grid_after_ai_move, CellState.X)

            output = program.execute(f"{next_move.x + 1}  {next_move.y + 1}")

        return CheckResult.correct()

    @dynamic_test(repeat=5, order=13)
    def check_hard_vs_hard(self):

        program = TestedProgram()
        program.start()

        output = program.execute("start hard hard")

        if "draw" not in output.lower():
            return CheckResult.wrong(
                "The result of the game between minimax algorithms should be always 'Draw'!\n"
                "Make sure your output contains 'Draw'.")

        return CheckResult.correct()


if __name__ == '__main__':
    TicTacToeTests().run_tests()
