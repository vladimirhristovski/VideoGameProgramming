import pygame
import sys

# --- CONFIG ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 60
GRID_COLS = 8
GRID_ROWS = 6
STATUS_BAR = 80
FPS = 30

# Colors
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
DARKGRAY = (50, 50, 50)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# States
STATE_REVEAL = "REVEAL"
STATE_PLAY = "PLAY"
STATE_OUT = "OUT"
STATE_END = "END"
STATE_WIN = "WIN"

# Timings
REVEAL_MS = 4000

# --- LEVEL ---
LEVEL = [
    "........",
    ".T..T..E",
    "....T...",
    ".TT.....",
    ".S......",
    "........"
]


def parse_level():
    traps = set()
    start = exitp = None
    for r, row in enumerate(LEVEL):
        for c, ch in enumerate(row):
            if ch == "S":
                start = [c, r]
            if ch == "E":
                exitp = (c, r)
            if ch == "T":
                traps.add((c, r))
    return start, exitp, traps


def grid_origin():
    w = GRID_COLS * CELL_SIZE
    h = GRID_ROWS * CELL_SIZE
    return (WINDOW_WIDTH - w) // 2, STATUS_BAR + (WINDOW_HEIGHT - STATUS_BAR - h) // 2


def draw_board(screen, player, exitp, traps, revealed_traps, state):
    screen.fill(BLACK)

    # Status bar
    pygame.draw.rect(screen, DARKGRAY, (0, 0, WINDOW_WIDTH, STATUS_BAR))

    gx, gy = grid_origin()

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rect = pygame.Rect(gx + c * CELL_SIZE, gy + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Determine cell color
            cell_color = GRAY
            is_trap = (c, r) in traps
            is_revealed = (c, r) in revealed_traps or state == STATE_REVEAL

            if (c, r) == exitp:
                cell_color = BLUE
            elif is_trap and is_revealed:
                cell_color = RED

            pygame.draw.rect(screen, cell_color, rect)
            pygame.draw.rect(screen, DARKGRAY, rect, 1)

            # Draw player
            if player[0] == c and player[1] == r:
                player_rect = pygame.Rect(rect.x + 10, rect.y + 10, CELL_SIZE - 20, CELL_SIZE - 20)
                pygame.draw.rect(screen, GREEN, player_rect)


def draw_status(screen, font, state, lives, player, message):
    # State indicator
    state_text = font.render(f"STATE: {state}", True, WHITE)
    screen.blit(state_text, (20, 10))

    # Lives
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WINDOW_WIDTH - 150, 10))

    # Position
    pos_text = font.render(f"Pos: ({player[0]}, {player[1]})", True, WHITE)
    screen.blit(pos_text, (WINDOW_WIDTH // 2 - 50, 10))

    # Message
    msg_surface = font.render(message, True, WHITE)
    msg_rect = msg_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
    screen.blit(msg_surface, msg_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Лавиринт со стапици")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    start, exitp, traps = parse_level()
    player = list(start)
    lives = 3
    state = STATE_REVEAL
    message = "Запомнете ги стапиците!"
    revealed_traps = set()

    state_start_time = pygame.time.get_ticks()

    while True:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        # Event handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                # ESC to quit
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Restart
                if e.key == pygame.K_r:
                    player = list(start)
                    lives = 3
                    state = STATE_REVEAL
                    message = "Запомнете ги стапиците!"
                    revealed_traps = set()
                    state_start_time = current_time

                # Movement (only in PLAY or OUT state)
                if state == STATE_PLAY or state == STATE_OUT:
                    new_x, new_y = player[0], player[1]

                    if e.key == pygame.K_UP:
                        new_y -= 1
                    elif e.key == pygame.K_DOWN:
                        new_y += 1
                    elif e.key == pygame.K_LEFT:
                        new_x -= 1
                    elif e.key == pygame.K_RIGHT:
                        new_x += 1
                    else:
                        continue

                    # Check boundaries
                    if new_x < 0 or new_x >= GRID_COLS or new_y < 0 or new_y >= GRID_ROWS:
                        state = STATE_OUT
                        message = "Не можете да излезете од таблата!"
                        continue

                    # Valid move - return to PLAY if was OUT
                    if state == STATE_OUT:
                        state = STATE_PLAY
                        message = "Движете се! (стрелки)"

                    if True:
                        player[0], player[1] = new_x, new_y

                        # Check trap
                        if (new_x, new_y) in traps:
                            lives -= 1
                            revealed_traps.add((new_x, new_y))

                            if lives <= 0:
                                state = STATE_END
                                message = "GAME OVER! Притиснете R за рестарт"
                            else:
                                message = f"Удривте во стапица! Животи: {lives}"

                        # Check exit
                        elif (new_x, new_y) == exitp:
                            state = STATE_WIN
                            message = "Победа! Притиснете R за рестарт"

        # State machine logic
        elapsed = current_time - state_start_time

        if state == STATE_REVEAL:
            if elapsed >= REVEAL_MS:
                state = STATE_PLAY
                message = "Движете се! (стрелки)"
                state_start_time = current_time

        # Draw everything
        draw_board(screen, player, exitp, traps, revealed_traps, state)
        draw_status(screen, font, state, lives, player, message)

        pygame.display.flip()


if __name__ == "__main__":
    main()