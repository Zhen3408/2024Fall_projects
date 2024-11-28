from player import HumanPlayer
from player import AIPlayer
from pentago import Pentago


if __name__ == "__main__":
    print('Choose which size of board you like:\n'
          '1. 6x6 Pentago: Four 3X3 quadrants, FIVE in a row wins.\n'
          '2. 8X8 Pentago: Four 4X4 quadrants, SIX in a row wins.')
    board_size = int(input('Input your choice:'))
    if board_size == 1:
        game = Pentago()
    else:
        game = Pentago(board_size=8, quadrant_size=4, win_length=6)

    print('Choose the game pattern you like:\n'
          '1. Human Player VS Human Player.\n'
          '2. Human Player VS Computer Player.\n'
          '3. Computer Player VS Computer Player.')
    game_mode = int(input('Input your choice:'))

    # initiate both players based on user choice
    player1 = HumanPlayer(player_id=1) if game_mode in [1,2] else AIPlayer(player_id=1)
    player2 = HumanPlayer(player_id=-1) if game_mode == 1 else AIPlayer(player_id=-1)

    while True:
        game.print_board()
        if game.current_player == player1.player_id:
            move = player1.get_move(game)
        else:
            move = player2.get_move(game)

        if move is None:  # when there's no legal move or game will be a draw anyway
            print("There's no legal move on board!")
            break

        game.make_move(*move)
        winner = game.check_winner()

        if game.is_draw(winner):
            print("This game is a draw!")
            game.print_board()
            break

        if winner:
            print(game.board)
            if winner == 1:
                print("Player #1 wins!")
            else:
                print("Player #2 wins!")
            break