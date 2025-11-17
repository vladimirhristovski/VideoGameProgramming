import pygame
import sys

from pygame.locals import *
pygame.init()


# DODADENI RABOTI
INVALID_COLOR = (255, 0, 0)
SUBGRID_LINE_WIDTH = 4
MESSAGE_FONT_SIZE = 28
MESSAGE_FONT = pygame.font.Font(None, MESSAGE_FONT_SIZE)
MARGIN = 100

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 4
CELL_SIZE = (WINDOW_SIZE - 2 * MARGIN) // GRID_SIZE
FONT_SIZE = 32
BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 255)
HIGHLIGHT_COLOR = (200, 200, 200)

DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku Solver")
FONT = pygame.font.Font(None, FONT_SIZE)

# Initial Sudoku Grid (0 represents empty cells)
SUDOKU_GRID = [
    [1, 0, 0, 4],
    [0, 0, 3, 0],
    [0, 4, 0, 0],
    [2, 0, 0, 3]
]


# Helper Functions
def draw_grid(grid, selected=None, message=''):
    """Draw the Sudoku grid with optional highlighting."""
    DISPLAYSURF.fill(BG_COLOR)

    if message:
        msg = MESSAGE_FONT.render(message, True, INVALID_COLOR)
        msg_rect = msg.get_rect(center=(WINDOW_SIZE // 2, 20))
        DISPLAYSURF.blit(msg, msg_rect)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            # TUKA E ZA DODAVANJE NA PADDING
            x = MARGIN + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(DISPLAYSURF, GRID_COLOR, rect, 1)
            if (row, col) == selected:
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, rect)

            # Draw numbers
            if grid[row][col] != 0:
                text_surface = FONT.render(str(grid[row][col]), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                DISPLAYSURF.blit(text_surface, text_rect)

    # TUKA DODAVAME LINII NA SUBGRIDOT
    subgrid_size = int(GRID_SIZE ** 0.5)
    for i in range(subgrid_size + 1):
        start = 100 + i * subgrid_size * CELL_SIZE
        pygame.draw.line(DISPLAYSURF, GRID_COLOR, (start, MARGIN), (start, MARGIN + GRID_SIZE * CELL_SIZE),
                         SUBGRID_LINE_WIDTH)
        pygame.draw.line(DISPLAYSURF, GRID_COLOR, (MARGIN, start), (MARGIN + GRID_SIZE * CELL_SIZE, start),
                         SUBGRID_LINE_WIDTH)


def is_valid_move(grid, row, col, num):
    """Checks if placing 'num' in grid[row][col] is valid."""
    # Check row
    if num in grid[row]:
        return False
    # Check column
    if num in [grid[r][col] for r in range(GRID_SIZE)]:
        return False
    # Check subgrid
    subgrid_size = int(GRID_SIZE ** 0.5)
    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    for r in range(start_row, start_row + subgrid_size):
        for c in range(start_col, start_col + subgrid_size):
            if grid[r][c] == num:
                return False
    return True


def is_solved(grid):
    """Checks if the Sudoku grid is completely and correctly filled."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            grid[row][col] = 0
            if num == 0:
                return False
            if not is_valid_move(grid, row, col, num):
                grid[row][col] = num
                return False
            grid[row][col] = num
    return True


# Main Game Loop
def main():
    grid = [row[:] for row in SUDOKU_GRID]
    selected = None
    message = ''
    message_timer = 0
    clock = pygame.time.Clock()

    while True:
        draw_grid(grid, selected, message)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos

                # PROVERKA DALI E KLIKNATO VO GRIDOT
                if MARGIN <= x <= MARGIN + GRID_SIZE * CELL_SIZE and MARGIN <= y <= MARGIN + GRID_SIZE * CELL_SIZE:
                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN) // CELL_SIZE
                    selected = (row, col)
                else:
                    selected = None

            elif event.type == KEYDOWN and selected:
                row, col = selected
                if event.key == K_BACKSPACE or event.key == K_DELETE:
                    grid[row][col] = 0
                elif K_1 <= event.key <= K_9:
                    num = event.key - K_0
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if is_solved(grid):
                            message = 'Sudoku Solved!'
                            message_timer = 5000
                    else:
                        message = f'Invalid move at ({row+1}, {col+1})'
                        message_timer = 1000

        if message_timer >0:
            message_timer-= 1
        else:
            message = ''
        pygame.display.update()


if __name__ == "__main__":
    main()
