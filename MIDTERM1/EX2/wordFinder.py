import pygame
import random
import sys
from pygame.locals import *
from sqlalchemy import false

# Constants

MARGIN = 100

WINDOW_SIZE = 800
GRID_SIZE = 10  # Grid will be GRID_SIZE x GRID_SIZE
CELL_SIZE = (WINDOW_SIZE - 2 * MARGIN) // GRID_SIZE
FONT_SIZE = 40
BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 255)
HIGHLIGHT_COLOR = (200, 200, 200)
WORD_LIST = ["PYTHON", "GAME", "CODE", "FUN", "PUZZLE"]
BLACK = GRID_COLOR
CORRECT = (255, 250, 0)
pygame.init()
# pygame.font.init()

DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Word Finder Puzzle")
FONT = pygame.font.Font(None, FONT_SIZE)

CORRECT_CELLS = []

# Generate a random grid and place words
def generate_grid(word_list):
    """Generates a grid and places words."""
    grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Right, Down, Diagonal, Reverse Diagonal

    for word in word_list:
        placed = False
        print("Placing words")
        while not placed:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            direction = random.choice(directions)
            if can_place_word(grid, word, row, col, direction):
                place_word(grid, word, row, col, direction)
                placed = True

    # Fill remaining spaces with random letters
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == '':
                grid[row][col] = chr(random.randint(65, 90))  # Random A-Z
                print("Filling blank spaces)")

    return grid


def can_place_word(grid, word, row, col, direction):
    """Checks if a word can fit in the grid at the given position and direction."""
    dr, dc = direction
    for i in range(len(word)):
        r, c = row + i * dr, col + i * dc
        if r < 0 or c < 0 or r >= GRID_SIZE or c >= GRID_SIZE or (grid[r][c] not in ('', word[i])):
            return False
    return True


def place_word(grid, word, row, col, direction):
    """Places a word into the grid."""
    dr, dc = direction
    for i in range(len(word)):
        r, c = row + i * dr, col + i * dc
        grid[r][c] = word[i]


def draw_grid(grid, selected_cells=None):
    """Draws the grid and highlights selected cells."""
    DISPLAYSURF.fill(BG_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Highlight selected cells
            if selected_cells and (row, col) in selected_cells:
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, rect)
            if CORRECT_CELLS and (row, col) in CORRECT_CELLS:
                pygame.draw.rect(DISPLAYSURF, CORRECT, rect)
            pygame.draw.rect(DISPLAYSURF, GRID_COLOR, rect, 1)  # Draw grid lines
            letter = grid[row][col]
            if letter:
                text_surface = FONT.render(letter, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                DISPLAYSURF.blit(text_surface, text_rect)


def is_word_valid(grid, selected_cells, word_list):
    """Checks if the selected cells form a valid word."""
    word = ''.join(grid[row][col] for row, col in selected_cells)
    return word in word_list


def drawMissingWords(foundWords):
    missingWords = [word for word in WORD_LIST if word not in foundWords]
    missingWordsString = ", ".join(missingWords)
    msg = FONT.render(missingWordsString, True, BLACK)
    msg_rect = msg.get_rect(center=(WINDOW_SIZE // 2, 20))
    DISPLAYSURF.blit(msg, msg_rect)


def checkSelected(selectedCells, newX, newY):
    # DOZVOLA ZA SELEKTIRANJE NA BUKVI SAMO VO EDNA NASOKA
    if len(selectedCells) > 1:
        for i in range(len(selectedCells)):
            if i != 0:
                fx, fy = selectedCells[i - 1]
                sx, sy = selectedCells[i]
                nx, ny = sx - fx, sy - fy
                for ox, oy in selectedCells:
                    x, y = ox + nx, oy + ny
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if newX == x and newY == y:
                            return True
                    x, y = ox - nx, oy - ny
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if newX == x and newY == y:
                            return True
        return False
    return True

def paintBox(row,col):
    rect = pygame.Rect(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAYSURF, CORRECT, rect)


# Main game loop
def main():
    grid = generate_grid(WORD_LIST)
    selected_cells = []
    found_words = set()
    score = 0

    while True:
        draw_grid(grid, selected_cells)
        drawMissingWords(found_words)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = (y - MARGIN) // CELL_SIZE, (x - MARGIN) // CELL_SIZE
                if (row, col) not in selected_cells:
                    if checkSelected(selected_cells, row, col):
                        selected_cells.append((row, col))
                else:
                    selected_cells.remove((row, col))
            elif event.type == KEYUP:
                if event.key == K_RETURN:
                    word = ''.join(grid[row][col] for row, col in selected_cells)
                    if word in WORD_LIST and word not in found_words:
                        found_words.add(word)
                        score += len(word)
                        print(f"Found Word: {word}. Score: {score}")
                        for r, c in selected_cells:
                            CORRECT_CELLS.append((r,c))  # Mark found letters
                    else:
                        print("Invalid or already found word!")
                    selected_cells = []
                elif event.key == K_h:  # Hint system
                    remaining_words = [word for word in WORD_LIST if word not in found_words]
                    if remaining_words:
                        hint_word = random.choice(remaining_words)
                        print(f"Hint: Look for '{hint_word[0]}'")
                    else:
                        print("No more hints available!")


if __name__ == "__main__":
    main()
