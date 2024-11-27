import random
import math
import numpy as np
from typing import Union, List


class Pentago:
    def __init__(self):
        """
        :param current_player:
        :param quadrant_start: indicate the top-left corner cell coordinate of each quadrant, there are four quadrants ,
        I assume the top-left one is number 0, top-right one is number 1, bottom-left one is number 2, and bottom-right
        one is number 3.
        """
        self.board_size = 6
        self.board = np.array([[0] * self.board_size for _ in range(self.board_size)])
        self.quadrant_start = [(0, 0), (0, 3), (3, 0), (3, 3)]
        self.current_player = 1
        self.win_length = 5

    def rotate_quadrant(self, quadrant: int, direction: int) -> bool:
        """
        :param quadrant: the quadrant number to rotate
        :param direction: 1 for clockwise, -1 for counterclockwise
        :return: bool
        """
        start_row, start_col = self.quadrant_start[quadrant]
        sub_board = self.board[start_row: start_row+3, start_col: start_col+3]
        if direction == 1:
            rotated = np.rot90(sub_board, k=-1)  # clockwise rotate
        elif direction == -1:
            rotated = np.rot90(sub_board, k=1)
        else:
            return False
        # substitute the rotated sub board back to the big board
        self.board[start_row: start_row+3, start_col: start_col+3] = rotated
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
        check if exist 5 consecutive marble on board
        for diagonal check, I find all diagonal starting cell coordinate on top of the board, whether top-left to
        bottom-right or top-right to bottom-left
        :return: False if exist no winner, player number of winner if exist winner
        """
        diagonal_range = self.board_size - self.win_length + 1
        left_start_points = []
        right_start_points = []
        for i in range(diagonal_range):
            for j in range(diagonal_range):
                top_left = (i, j)
                top_right = (i, self.board_size-1-j)
                left_start_points.append(top_left)
                right_start_points.append(top_right)

        for player in [-1, 1]:
            for i in range(self.board_size):  # column and rows check
                if self.check_consecutive(self.board[i,:], player):
                    return player
                if self.check_consecutive(self.board[:,i], player):
                    return player

            for cell in left_start_points:  # left to right diagonal
                if self.check_diagonal(cell, player, 1):
                    return player
            for cell in right_start_points:  # right to left diagonal
                if self.check_diagonal(cell, player, -1):
                    return player

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

# if __name__ == "__main__":
#     game = Pentago()
#     game.board = np.array([
#         [1, 1, 1, 1, -1, 1],
#         [-1, -1, -1, 1, -1, 1],
#         [-1, -1, -1, 1, -1, -1],
#         [1, -1, 1, 1, 1, 1],
#         [1, -1, 1, -1, -1, -1],
#         [-1, 1, -1, 1, -1, 1]
#     ])
#
#     print("Is draw:", game.is_draw(game.check_winner()))  #  True
