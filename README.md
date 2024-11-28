# Pentago - Zhen Li

## Project Type: Developing an AI game player for an original variation of the Pentago game

## Pentago Introduction:

Pentago is an abstract strategy game for two players with four 3×3 grids arranged into a larger 6×6 grid. This game reimplements the well-known Connect 4 with a twist: After placing a marble, the player has the option to twist one of the grids by 90°, thus changing the board after every turn. The first player to get five marbles in a row wins.

## Game Variation:

The variation I built upon the original Pentago is changing the board to four 4×4 grids arranged into a larger 8×8 grid, meanwhile, the winning condition changes to SIX marbles in a row. This larger layout enables players a larger space to play against each other and thinking of strategy. Compared to original smaller board, it's less likely to achieve a draw.

## AI Player Implementation:

The AI player is implemented based on Minimax algorithm and alpha-beta pruning.

## How to Start Game:

Execute the ```play_game.py``` file, follow the text prompt to choose whether play 6X6 or 8X8 board size. Then choose the game mode either play computer-vs-computer and/or against human players. When you play as a human player, input the move you want in this format: ```row, col, quadrant, direction```. ```row``` and ```col``` index is labeled in the printed text board. For ```quadrant```,  the top-left quadrant is number 0, top-right quadrant is number 1, bottom-left quadrant is number 2, and bottom-right quadrant is number 3. For ```direction```, 1 means rotate clockwise, -1 means rotate counterclockwise. For example, if you input ```1, 2, 1, -1```, your move is placing a piece on the cell of row 1 column 2 and then rotate the quadrant on top-right counterclockwise.
