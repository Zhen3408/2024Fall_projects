from pentago import Pentago


class HumanPlayer:
    def __init__(self, player_id: int):
        """
        :param player_id: 1 for Player 1, -1 for Player 2
        """
        self.player_id = player_id

    def get_move(self, game: Pentago) -> tuple[int, int, int, int]:
        """
        Prompts the player for their move.
        :param game: The current game instance, for validating input and displaying board state.
        :return: A tuple (row, col, quadrant, direction)
        """
        print(f"Player {self.player_id} turn:")
        while True:
            try:
                # Display the board
                print(game.board)
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