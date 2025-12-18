import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 720
GRID_SIZE = 8
CELL_SIZE = 640 // GRID_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")
clock = pygame.time.Clock()

CANDIES = []
for i in range(1, 5):
    img = pygame.image.load(f'candy{i}.png')
    img = pygame.transform.scale(img, (CELL_SIZE - 10, CELL_SIZE - 10))
    CANDIES.append(img)

grid = [[random.randint(0, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

selected = None
score = 0
font = pygame.font.Font(None, 48)


def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            pygame.draw.rect(screen, (70, 70, 70), (x, y, CELL_SIZE, CELL_SIZE), 1)

            if grid[row][col] != -1:
                candy_img = CANDIES[grid[row][col]]
                screen.blit(candy_img, (x + 5, y + 5))

            if selected == (row, col):
                pygame.draw.rect(screen, (255, 255, 255), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 4)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, HEIGHT - 60))


def check_matches_around(pos):
    row, col = pos
    all_matches = set()

    if grid[row][col] == -1:
        return all_matches

    candy_type = grid[row][col]

    left = col
    while left > 0 and grid[row][left - 1] == candy_type:
        left -= 1

    right = col
    while right < GRID_SIZE - 1 and grid[row][right + 1] == candy_type:
        right += 1

    if right - left + 1 >= 3:
        for c in range(left, right + 1):
            all_matches.add((row, c))

    top = row
    while top > 0 and grid[top - 1][col] == candy_type:
        top -= 1

    bottom = row
    while bottom < GRID_SIZE - 1 and grid[bottom + 1][col] == candy_type:
        bottom += 1

    if bottom - top + 1 >= 3:
        for r in range(top, bottom + 1):
            all_matches.add((r, col))

    return all_matches


def check_matches():
    matches = set()

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] != -1 and grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.add((row, col))
                matches.add((row, col + 1))
                matches.add((row, col + 2))

    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] != -1 and grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.add((row, col))
                matches.add((row + 1, col))
                matches.add((row + 2, col))

    return matches


def calculate_score(match_count):
    if match_count >= 12:
        return 3
    elif match_count >= 6:
        return 2
    elif match_count >= 3:
        return 1
    return 0


def remove_matches(matches):
    for row, col in matches:
        grid[row][col] = -1


def drop_candies():
    for col in range(GRID_SIZE):
        empty = []
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] == -1:
                empty.append(row)
            elif empty:
                grid[empty[-1]][col] = grid[row][col]
                grid[row][col] = -1
                empty.pop()
                empty.insert(0, row)


def fill_empty():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == -1:
                grid[row][col] = random.randint(0, 3)


def swap_candies(pos1, pos2):
    grid[pos1[0]][pos1[1]], grid[pos2[0]][pos2[1]] = grid[pos2[0]][pos2[1]], grid[pos1[0]][pos1[1]]


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            col = mx // CELL_SIZE
            row = my // CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if selected is None:
                    selected = (row, col)
                else:
                    r1, c1 = selected
                    if (abs(r1 - row) == 1 and c1 == col) or (abs(c1 - col) == 1 and r1 == row):
                        swap_candies(selected, (row, col))

                        matches = check_matches_around(selected)
                        matches.update(check_matches_around((row, col)))

                        if matches:
                            score += calculate_score(len(matches))
                            remove_matches(matches)
                            drop_candies()
                            fill_empty()

                            while True:
                                matches = check_matches()
                                if not matches:
                                    break
                                score += calculate_score(len(matches))
                                remove_matches(matches)
                                drop_candies()
                                fill_empty()

                    selected = None

    screen.fill((40, 40, 40))
    draw_grid()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()