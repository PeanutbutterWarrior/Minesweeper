import random


def generate_board(w, h, mines):
    new_board = [[0 for _ in range(w)] for _ in range(h)]
    info = [[(False, False) for _ in range(w)] for _ in range(h)]
    mine_positions = random.sample(range(w * h), mines)

    for position in mine_positions:
        x, y = position % h, position // h
        new_board[y][x] = -1
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < w and 0 <= y + dy < h and new_board[y + dy][x + dx] != -1:
                    new_board[y + dy][x + dx] += 1

    return new_board, info


width = int(input('Width: '))
height = int(input('Height: '))
num_mines = int(input('Number of mines: '))
board, board_info = generate_board(width, height, num_mines)
