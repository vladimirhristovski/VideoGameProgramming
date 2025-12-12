import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()

try:
    spaceship_img = pygame.image.load("spaceship.png")
    spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
    asteroid_base_img = pygame.image.load("asteroid.png")
    crystal_img = pygame.image.load("energy_crystal.png")
    crystal_img = pygame.transform.scale(crystal_img, (30, 30))

    pygame.mixer.music.load("background_music.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    clash_sound = pygame.mixer.Sound("clash_sound.wav")
    clash_sound.set_volume(0.5)
except:
    print("Грешка при вчитување на ресурси!")
    sys.exit()


class Player:
    def __init__(self):
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)

    def update(self, keys, fall_speed):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= fall_speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += fall_speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= fall_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += fall_speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Asteroid:
    def __init__(self, size):
        self.size = size
        self.image = pygame.transform.scale(asteroid_base_img, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - size)
        self.rect.y = random.randint(-100, -size)

    def update(self, fall_speed):
        self.rect.y += fall_speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Crystal:
    def __init__(self):
        self.image = crystal_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)

    def update(self, fall_speed):
        self.rect.y += fall_speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def initialization():
    return Player(), [], [], 0, 0, 30, 3, 180


font = pygame.font.Font(None, 36)
player, asteroids, crystals, score, timer, asteroid_size, fall_speed, difficulty_increase_interval = initialization()
running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                player, asteroids, crystals, score, timer, asteroid_size, fall_speed, difficulty_increase_interval = initialization()
                game_over = False
    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys, fall_speed)

        timer += 1
        if timer % difficulty_increase_interval == 0:
            fall_speed += 0.5
            asteroid_size = min(asteroid_size + 5, 100)

        if timer % 40 == 0:
            asteroids.append(Asteroid(asteroid_size))
            asteroid_timer = 0

        if timer % 60 == 0:
            crystals.append(Crystal())
            crystal_timer = 0

        for asteroid in asteroids[:]:
            asteroid.update(fall_speed)
            if asteroid.rect.top > HEIGHT:
                asteroids.remove(asteroid)
            elif player.rect.colliderect(asteroid.rect):
                clash_sound.play()
                game_over = True

        for crystal in crystals[:]:
            crystal.update(fall_speed)
            if crystal.rect.top > HEIGHT:
                crystals.remove(crystal)
            elif player.rect.colliderect(crystal.rect):
                crystals.remove(crystal)
                score += 1

    screen.fill(BLACK)

    if not game_over:
        player.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for crystal in crystals:
            crystal.draw(screen)

        score_text = font.render(f"Кристали: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        game_over_text = font.render("КРАЈ НА ИГРА!", True, WHITE)
        score_text = font.render(f"Кристали: {score}", True, WHITE)
        restart_text = font.render("Притисни SPACE за нова игра", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()