import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Aim Trainer")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load the target and player images
target_image = pygame.image.load("target.png")
player_image = pygame.image.load("player.png")

# Define target properties
TARGET_RADIUS = target_image.get_width() // 2
TARGET_COLOR = GREEN
TARGET_SPEED = 3

# Player properties
PLAYER_RADIUS = player_image.get_width() // 2
PLAYER_COLOR = WHITE

# Game variables
score = 0
game_start_time = pygame.time.get_ticks()
game_duration = 60000  # 60 seconds
game_over = False

# Function to draw the target
def draw_target(x, y):
    screen.blit(target_image, (x - target_image.get_width() // 2, y - target_image.get_height() // 2))

# Function to draw the player
def draw_player(x, y):
    screen.blit(player_image, (x - player_image.get_width() // 2, y - player_image.get_height() // 2))

# Main game loop
running = True
target_x = random.randint(TARGET_RADIUS, WINDOW_WIDTH - TARGET_RADIUS)
target_y = random.randint(TARGET_RADIUS, WINDOW_HEIGHT - TARGET_RADIUS)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Check if the player clicked on the target
            mouse_x, mouse_y = event.pos
            if (mouse_x - target_x) ** 2 + (mouse_y - target_y) ** 2 <= TARGET_RADIUS ** 2:
                score += 1
                target_x = random.randint(TARGET_RADIUS, WINDOW_WIDTH - TARGET_RADIUS)
                target_y = random.randint(TARGET_RADIUS, WINDOW_HEIGHT - TARGET_RADIUS)

    # Move the target
    if not game_over:
        target_x += random.randint(-TARGET_SPEED, TARGET_SPEED)
        target_y += random.randint(-TARGET_SPEED, TARGET_SPEED)

        # Keep the target within the window
        target_x = max(TARGET_RADIUS, min(target_x, WINDOW_WIDTH - TARGET_RADIUS))
        target_y = max(TARGET_RADIUS, min(target_y, WINDOW_HEIGHT - TARGET_RADIUS))

        # Update the time remaining
        if not game_over:
            elapsed_time = pygame.time.get_ticks() - game_start_time
            time_remaining = max(0, game_duration - elapsed_time)
            if time_remaining == 0:
                game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the target
    draw_target(target_x, target_y)

    # Draw the player
    player_x, player_y = pygame.mouse.get_pos()
    draw_player(player_x, player_y)

    # Display the score and time remaining
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render(f"Time: {time_remaining // 1000}", True, WHITE)
    screen.blit(text, (10, 40))

    if game_over:
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()