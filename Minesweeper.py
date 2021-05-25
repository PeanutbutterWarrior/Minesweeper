import pygame
import random


def generate_board(w, h, mines):
    new_board = [[0 for _ in range(w)] for _ in range(h)]
    info = [[[False, False] for _ in range(w)] for _ in range(h)]
    mine_positions = random.sample(range(w * h), mines)

    for position in mine_positions:
        x, y = position % h, position // h
        new_board[y][x] = -1
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < w and 0 <= y + dy < h and new_board[y + dy][x + dx] != -1:
                    new_board[y + dy][x + dx] += 1

    return new_board, info


def draw(grid, info,  screen):
    screen.fill((181, 181, 181))
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if info[y][x][0]:
                if cell >= 1:
                    screen.blit(number_images[cell - 1], (x * 24, y * 24))
                elif cell == -1:
                    screen.blit(bomb, (x * 24, y * 24))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x * 24, y * 24, 21, 21))
                pygame.draw.rect(screen, (210, 210, 210), (x * 24 + 3, y * 24 + 3, 18, 18))
                if info[y][x][1]:
                    screen.blit(flag, (x * 24, y * 24))

    for y in range(height - 1):
        pygame.draw.line(screen, (0, 0, 0), (0, y * 24 + 22), (width * 24, y * 24 + 22), 3)

    for x in range(width - 1):
        pygame.draw.line(screen, (0, 0, 0), (x * 24 + 22, 0), (x * 24 + 22, height * 24), 3)


def floodfill(start, grid, info):
    to_expand = [start]
    while to_expand:
        x, y = to_expand.pop(-1)
        if not info[y][x][1] and not info[y][x][0]:
            info[y][x][0] = True
            if grid[y][x] == 0:
                for dx in range(-1, 2):
                    if x + dx < 0 or x + dx >= len(grid[0]):
                        continue
                    for dy in range(-1, 2):
                        if not dx == dy == 0 and 0 <= y + dy < len(grid):
                            to_expand.append((x + dx, y + dy))


width = int(input('Width: '))
height = int(input('Height: '))
num_mines = int(input('Number of mines: '))
board, board_info = generate_board(width, height, num_mines)

pygame.init()
font = pygame.font.SysFont('Comic Sans', 25, True, False)

number_images = []
text_colors = ('#0000ff', '#00ce1e', '#D81111', '#9002e2', '#e5ca00', '#04d3d3', '#707070', '#ffffff')
for number, color in zip(range(1, 10), text_colors):
    correct_size_surface = pygame.Surface((21, 21))
    number_surface = font.render(str(number), False, pygame.Color(color))
    size = number_surface.get_size()
    correct_size_surface.blit(number_surface, ((21 - size[0]) // 2, (21 - size[1]) // 2))
    correct_size_surface.set_colorkey((0, 0, 0))
    number_images.append(correct_size_surface)

bomb = pygame.image.load('bomb.png')
flag = pygame.image.load('flag.png')

screen = pygame.display.set_mode((width * 24 - 3, height * 24 - 3))
pygame.display.set_caption('Minesweeper')
pygame.display.set_icon(bomb)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            click_x, click_y = event.pos
            if click_x % 24 <= 21 and click_y % 24 <= 21:
                click_x, click_y = click_x // 24, click_y // 24

                if event.button == 1:
                    # Not flagged and not revealed
                    if not board_info[click_y][click_x][0] and not board_info[click_y][click_x][1]:
                        if board[click_y][click_x] == -1:
                            for i in board_info:
                                for j in i:
                                    j[0] = True
                        else:
                            floodfill((click_x, click_y), board, board_info)
                elif event.button == 3:
                    if not board_info[click_y][click_x][0]:
                        # Places/removes flag
                        board_info[click_y][click_x][1] = not board_info[click_y][click_x][1]

    draw(board, board_info, screen)
    pygame.display.flip()