import pygame
import sys

pygame.init()

# --- Settings ---
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 5, 5
SQUARE_SIZE = 80
BOARD_TOP_LEFT = (100, 100)

COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0)  # Yellow
]

BACKGROUND = (220, 220, 220)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Board Game")

font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 32)

board = [[None for _ in range(COLS)] for _ in range(ROWS)]
selected_color = None


def draw_board():
    pygame.draw.rect(screen, BLACK, (BOARD_TOP_LEFT[0], BOARD_TOP_LEFT[1], COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE))
    for r in range(ROWS):
        for c in range(COLS):
            x = BOARD_TOP_LEFT[0] + c * SQUARE_SIZE
            y = BOARD_TOP_LEFT[1] + r * SQUARE_SIZE
            color = board[r][c] if board[r][c] is not None else (255, 255, 255)
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)


def draw_palette():
    global selected_color
    text = small_font.render("Select a Color:", True, BLACK)
    screen.blit(text, (100, 520))

    for i, color in enumerate(COLORS):
        x = 100 + i * 114
        y = 560
        pygame.draw.rect(screen, color, (x, y, 60, 60))
        pygame.draw.rect(screen, BLACK, (x, y, 60, 60), 2)

        # Highlight selected color
        if selected_color == color:
            pygame.draw.rect(screen, BLACK, (x - 4, y - 4, 68, 68), 3)


def neighbors_same_color(r, c):
    color = board[r][c]
    if color is None:
        return False

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if board[nr][nc] == color:
                return True
    return False


def board_filled():
    return all(all(cell is not None for cell in row) for row in board)


def end_screen(text):
    screen.fill(BLACK)
    msg = font.render(text, True, (255, 255, 255))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)
    sys.exit()


# --- Main Loop ---
while True:
    screen.fill(BACKGROUND)

    title = font.render("Color Fill Puzzle", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    draw_board()
    draw_palette()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Select color
            for i, color in enumerate(COLORS):
                x = 100 + i * 114
                y = 560
                if x <= mx <= x + 100 and y <= my <= y + 100:
                    selected_color = color

            # Paint board cell
            if selected_color is not None:
                for r in range(ROWS):
                    for c in range(COLS):
                        x = BOARD_TOP_LEFT[0] + c * SQUARE_SIZE
                        y = BOARD_TOP_LEFT[1] + r * SQUARE_SIZE
                        if x <= mx <= x + SQUARE_SIZE and y <= my <= y + SQUARE_SIZE:
                            board[r][c] = selected_color
                            if neighbors_same_color(r, c):
                                end_screen("GAME OVER")

    if board_filled():
        end_screen("YOU WON!")

    pygame.display.update()
