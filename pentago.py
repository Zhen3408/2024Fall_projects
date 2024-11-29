import random
import math
import numpy as np
from typing import Union, List


class Pentago:
    def __init__(self, board_size=6, quadrant_size=3, win_length=5):
        """
        :param board_size: the original Pentago is 6X6 size
        :param quadrant_size: original quadrant_size is 3X3
        :param win_length: original win condition is 5 in a row
        :param current_player: set the first player's id as 1
        :param game_round: indicate which round the game is at
        :param quadrant_start: indicate the top-left corner cell coordinate of each quadrant, there are four quadrants ,
        I assume the top-left quadrant is number 0, top-right quadrant is number 1, bottom-left quadrant is number 2,
        and bottom-right quadrant is number 3.
        """
        self.board_size = board_size
        self.quadrant_size = quadrant_size
        self.win_length = win_length
        self.board = np.array([[0] * self.board_size for _ in range(self.board_size)])
        self.quadrant_start = [(0, 0), (0, quadrant_size), (quadrant_size, 0), (quadrant_size, quadrant_size)]
        self.current_player = 1
        self.game_round = 1

    def rotate_quadrant(self, quadrant: int, direction: int) -> bool:
        """
        :param quadrant: the quadrant number to rotate
        :param direction: 1 for clockwise, -1 for counterclockwise
        :return: bool
        """
        start_row, start_col = self.quadrant_start[quadrant]
        sub_board = self.board[start_row: start_row+self.quadrant_size, start_col: start_col+self.quadrant_size]
        if direction == 1:
            rotated = np.rot90(sub_board, k=-1)  # clockwise rotate
        elif direction == -1:
            rotated = np.rot90(sub_board, k=1)
        else:
            return False
        # substitute the rotated sub board back to the big board
        self.board[start_row: start_row+self.quadrant_size, start_col: start_col+self.quadrant_size] = rotated
        return True

    def make_move(self, row, col, quadrant, direction) -> bool:
        """
        place a marble on board
        choose a quadrant to rotate, either clockwise or counterclockwise
        """
        if not self.is_move_legal(row, col, quadrant, direction):
            return False
        self.board[row][col] = self.current_player
        self.rotate_quadrant(quadrant, direction)
        self.current_player *= -1
        self.game_round += 1
        return True

    def is_move_legal(self, row, col, quadrant, direction) -> bool:
        if self.board[row][col] != 0:
            return False
        elif quadrant not in range(len(self.quadrant_start)):
            return False
        elif direction not in [-1, 1]:
            return False
        return True

    def check_consecutive(self, array, player_marble: int) -> bool:
        """
        :param array: a row or column on board
        :param player_marble: the marble of this player
        :return: bool, whether exist 5 marble in a row
        """
        count = 0
        for i in array:
            if i == player_marble:
                count += 1
                if count == self.win_length:
                    return True
            else:
                count = 0
        return False

    def check_diagonal(self, start_point: tuple, player_marble: int, direction: int) -> bool:
        """
        :param start_point: the starting coordinate of diagonal
        :param player_marble: marble indicate player
        :param direction: 1 indicate start from top-left to bottom-right, -1 indicates start from top-right to bottom-left
        :return: bool
        """
        row, col = start_point
        count = 0
        for i in range(self.board_size):
            row = row + 1
            col = col + direction
            if row >= self.board_size or col >= self.board_size or col < 0:
                break
            elif self.board[row][col] == player_marble:
                count += 1
                if count == self.win_length:
                    return True
            else:
                count = 0
        return False


    def check_winner(self) -> Union[int, bool]:
        """
        Check if exist 5 consecutive marble on board
        For diagonal check, find all diagonal starting cell coordinate on top of the board, whether top-left to
        bottom-right or top-right to bottom-left。
        If both players achieve the win condition simultaneously after a quadrant rotation, it is a draw.
        :return: False if exist no winner, player number of winner if exist winner
        """
        diagonal_range = self.board_size - self.win_length + 1
        left_start_points = [(0, self.board_size-1)]  # top left corner
        right_start_points = [(0, 0)]  # top right corner
        for i in range(0, diagonal_range):
            left = [(i, 0), (0, i)]
            right = [(i, self.board_size-1), (0, self.board_size-1-i)]
            left_start_points += left
            right_start_points += right

        winner = set()

        for player in [-1, 1]:
            for i in range(self.board_size):  # column and rows check
                if self.check_consecutive(self.board[i,:], player):
                    winner.add(player)
                if self.check_consecutive(self.board[:,i], player):
                    winner.add(player)

            for cell in left_start_points:  # left to right diagonal
                if self.check_diagonal(cell, player, 1):
                    winner.add(player)
            for cell in right_start_points:  # right to left diagonal
                if self.check_diagonal(cell, player, -1):
                    winner.add(player)

        if len(winner) > 1:
            return "draw"  # both players win simultaneously, it's a draw
        elif len(winner) == 1:
            return winner.pop()  # only one player wins

        return False

    def is_draw(self, winner) -> bool:
        """
        check if the board is full and no winner
        :return True if board is full and exists no winner, False if exists winner
        """
        if winner is False and not (self.board == 0).any():
            return True
        return False

    def get_empty_positions(self) -> list[tuple]:
        """
        Returns a list of all empty positions (value=0) on the board using numpy.
        :return: List of (row, col) tuples representing empty positions.
        """
        return [tuple(pos) for pos in np.argwhere(self.board == 0)]

    def print_board(self) -> None:
        """
        Print the board in a formatted way.
        'B' (black) represent pieces of player 1 and 'W' (white) represent prices of player 2
        """
        board_size = self.board_size
        # Print column headers
        header = "   " + "   ".join(str(i) for i in range(board_size))
        print(header)
        print("  " + "----" * (board_size - 1) + "----")  # Top border

        for row in range(board_size):
            row_content = []
            for col in range(board_size):
                cell = self.board[row, col]
                if cell == 1:
                    row_content.append(" B ")
                elif cell == -1:
                    row_content.append(" W ")
                else:
                    row_content.append("   ")

            row_str = "|".join(row_content)
            # Print row with row number
            print(f"{row} |{row_str}|")
            print("  " + "----" * (board_size - 1) + "----")


# if __name__ == "__main__":
#     game = Pentago()
#     game.board = np.array([
#         [1, -1, 0, 1, 1, 0],
#         [1, -1, 0, -1, -1, 0],
#         [1, -1, 0, 1, -1, 0],
#         [1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0]
#     ])
#     game.make_move(5, 5, 0, 1)
#
#     print(game.check_winner())
