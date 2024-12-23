from pentago import Pentago
import numpy as np
from typing import Tuple, Optional
import random


class HumanPlayer:
    def __init__(self, player_id: int):
        """
        :param player_id: 1 for Player 1, -1 for Player 2
        """
        self.player_id = player_id
        self.player_number = 1 if self.player_id == 1 else 2  # for clear print

    def get_move(self, game: Pentago) -> tuple[int, int, int, int]:
        """
        Prompts the player for their move.
        :param game: The current game instance, for validating input and displaying board state.
        :return: A tuple (row, col, quadrant, direction)
        """
        print(f"Round{game.game_round} - Human Player #{self.player_number} turn:")
        while True:
            try:
                # Get user input
                move_input = input("Enter your move (row, col, quadrant, direction): ")
                row, col, quadrant, direction = map(int, move_input.split())
                # Validate the move
                if game.is_move_legal(row, col, quadrant, direction):
                    return row, col, quadrant, direction
                else:
                    print("Invalid move! Please try again.")
            except ValueError:
                print("Invalid input format. Please enter 4 integers separated by spaces.")


class AIPlayer:
    """
    AI Player implemented with Minimax and alpha-bera pruning.
    The minimax search depth is set as 2, which only consider the heuristic scores of one layer of this AI player
    and deeper layer of the opponent player. I have tried set larger depth, but the time complexity would be too huge
    to run.
    """
    def __init__(self, player_id: int, depth: int = 2):
        """
        :param player_id: 1 for Player 1, -1 for Player 2
        :param depth: Maximum depth for Minimax search
        """
        self.player_id = player_id
        self.player_number = 1 if self.player_id == 1 else 2  # for clear print
        self.depth = depth

    def get_move(self, game: Pentago) -> tuple[int, int, int, int] | None:
        """
        Determines the best move using Minimax with Alpha-Beta Pruning.
        :param game: The current game instance.
        :return: A tuple (row, col, quadrant, direction)
        """
        print(f"Round{game.game_round} - AI Player #{self.player_number} turn!")
        early_stage = game.board_size  # set early stage round based on board size, prevent 'slow' early decision in 8X8
        if game.board_size == 8 and game.game_round <= early_stage:  # when get into later stage of game, simulate deeper
            self.depth = 1
        else:
            self.depth = 2
        best_value, best_move = self.minimax(game, self.depth, -float('inf'), float('inf'), True)

        if best_move is None:
            #  No optimal move left. Choosing a random legal move to fill the board.
            try:
                empty_positions = game.get_empty_positions()
                row, col = random.choice(empty_positions)
                quadrant = random.choice([0, 1, 2, 3])
                direction = random.choice([-1, 1])
                best_move = (row, col, quadrant, direction)
            except:
                return None

        print(f"AI Players move detail: \n"
              f"row {best_move[0]}, "
              f"col {best_move[1]}, "
              f"rotate quadrant {best_move[2]}, "
              f"rotate direction {best_move[3]}")
        return best_move

    def minimax(self, game: Pentago, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[int, Optional[Tuple[int, int, int, int]]]:
        """
        Minimax algorithm with Alpha-Beta Pruning.
        :param game: Current game state.
        :param depth: Current search depth.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param maximizing: True if maximizing player's turn.
        :return: Tuple of (score, move)
        """
        winner = game.check_winner()
        if winner or depth == 0:
            return self.heuristic(game), None

        if game.is_draw(winner):
            return 0, None

        best_value = -float('inf') if maximizing else float('inf')
        best_move = None

        for row in range(game.board_size):
            for col in range(game.board_size):
                if game.board[row][col] == 0:
                    for quadrant in range(4):
                        for direction in [-1, 1]:
                            # Simulate the move
                            game.board[row][col] = self.player_id if maximizing else -self.player_id
                            game.rotate_quadrant(quadrant, direction)

                            value, _ = self.minimax(game, depth - 1, alpha, beta, not maximizing)

                            # Undo the move
                            game.rotate_quadrant(quadrant, -direction)
                            game.board[row][col] = 0

                            if maximizing:
                                if value > best_value:
                                    best_value = value
                                    best_move = (row, col, quadrant, direction)
                                alpha = max(alpha, value)

                            else:
                                if value < best_value:
                                    best_value = value
                                    best_move = (row, col, quadrant, direction)
                                beta = min(beta, value)

                            if beta <= alpha:  # pruning, AI won't want to dig deeper
                                break

        if best_move is None:
            return 0, None
        return best_value, best_move

    def heuristic(self, game: Pentago) -> float | int:
        """
        Heuristic function to evaluate the board state.
        :param game: Current game state.
        :return: Score of the board for the AI player.
        """
        winner = game.check_winner()
        # once one side wins, return an extreme value as heuristic score
        if winner == self.player_id:
            return float('inf')
        elif winner == -self.player_id:
            return float('-inf')

        score = 0
        for player in [1, -1]:
            factor = 1 if player == self.player_id else -1

            # Rows and columns
            for i in range(game.board_size):
                score += factor * self.evaluate_line(game.board[i, :], player, game.win_length)
                score += factor * self.evaluate_line(game.board[:, i], player, game.win_length)

            # Diagonals
            for row in range(game.board_size - game.win_length + 1):
                for col in range(game.board_size - game.win_length + 1):
                    diag1 = np.diagonal(game.board[row:row + game.win_length, col:col + game.win_length])
                    diag2 = np.diagonal(np.fliplr(game.board[row:row + game.win_length, col:col + game.win_length]))
                    score += factor * self.evaluate_line(diag1, player, game.win_length)
                    score += factor * self.evaluate_line(diag2, player, game.win_length)
        return score

    def evaluate_line(self, line: np.ndarray, player: int, win_length: int) -> int:
        """
        Evaluates a single line (row, column, or diagonal) for potential scores.
        :param line: A line from the board.
        :param player: The player id to evaluate for (1 or -1).
        :param win_length: The number of consecutive cells to achieve win
        :return: Score for the given line.
        """
        score = 0
        opponent = -player
        win_length = win_length
        player_count = 0
        opponent_count = 0

        # Initialize the first window
        for i in range(win_length):
            if line[i] == player:
                player_count += 1
            elif line[i] == opponent:
                opponent_count += 1

        # Score the first window
        if opponent_count == 0:
            score += 10 ** player_count
        elif player_count == 0:
            score -= 5 ** opponent_count

        # Slide the window across the line
        for i in range(win_length, len(line)):
            # Remove the element going out of the window
            if line[i - win_length] == player:
                player_count -= 1
            elif line[i - win_length] == opponent:
                opponent_count -= 1

            # Add the new element coming into the window
            if line[i] == player:
                player_count += 1
            elif line[i] == opponent:
                opponent_count += 1

            # Score the current window
            if opponent_count == 0:
                score += 10 ** player_count
            elif player_count == 0:
                score -= 5 ** opponent_count

        return score
