import math
import random

from common import tile


def board(board):
    board_size = len(board)
    print(board_size)
    side = int(math.sqrt(board_size))

    for r in range(side):
        for c in range(side):
            tile = board[r*side + c]
            info = tile.team_id if tile.revealed else tile.word
            print(info),
        print


if __name__ == "__main__":
    tiles = [tile(random.choice(string.ascii_letters), random.randint(0, 2), False) for _ in range(9)]
    for t in tiles:
        print(t)
    board(tiles)
