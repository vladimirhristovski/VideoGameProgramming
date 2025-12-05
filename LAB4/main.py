import pygame
import random
import sys

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Assignment")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Game variables ---
paddle_width, paddle_height = 20, 120
paddle_x = 30
paddle_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 7

ball_size = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

score = 0
game_over = False
paused = False

font = pygame.font.SysFont("Arial", 32)


def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score, game_over
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 5
    ball_speed_y = 5
    score = 0
    game_over = False


clock = pygame.time.Clock()


# --- Main loop ---
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pause / Resume
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_r and game_over:
                reset_game()

    # Skip game updates when paused
    if paused or game_over:
        WIN.fill(BLACK)
        pause_text = ""

        if paused:
            pause_text = font.render("PAUSED - Press P to Continue", True, WHITE)
        elif game_over:
            pause_text = font.render(f"GAME OVER - Score: {score} | Press R to Restart", True, WHITE)

        WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2,
                              HEIGHT // 2 - pause_text.get_height() // 2))
        pygame.display.update()
        continue

    # --- Paddle movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_y > 0:
        paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_y < HEIGHT - paddle_height:
        paddle_y += paddle_speed

    # --- Ball movement ---
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce from top/bottom
    if ball_y <= 0 or ball_y >= HEIGHT - ball_size:
        ball_speed_y *= -1

    # Right side = wall bounce
    if ball_x >= WIDTH - ball_size:
        ball_speed_x *= -1

    # Ball passes the paddle → game loses
    if ball_x <= 0:
        game_over = True

    # Collision with paddle
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

    if ball_rect.colliderect(paddle_rect) and ball_speed_x < 0:
        ball_speed_x *= -1

        # Increase difficulty
        ball_speed_x += 0.5 if ball_speed_x > 0 else -0.5
        ball_speed_y += random.choice([-2, -1, 0, 1, 2])  # random vertical offset

        score += 1

    # --- Drawing ---
    WIN.fill(BLACK)

    # Paddle
    pygame.draw.rect(WIN, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Ball
    pygame.draw.rect(WIN, WHITE, (ball_x, ball_y, ball_size, ball_size))

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
