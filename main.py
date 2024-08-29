import pygame
import asyncio
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
target_image = pygame.transform.scale(target_image, (100, 100))
player_image = pygame.transform.scale(player_image, (50, 50))

# Define target properties
TARGET_RADIUS = target_image.get_width() // 2
TARGET_COLOR = GREEN
TARGET_SPEED = 3

# Player properties
PLAYER_RADIUS = player_image.get_width() // 2
PLAYER_COLOR = WHITE

# Game variables
score = 0
game_start_time = 0
game_duration = 20000  # 20 seconds
game_over = False
game_started = False

# Function to draw the target
def draw_target(x, y):
    screen.blit(target_image, (x - target_image.get_width() // 2, y - target_image.get_height() // 2))

# Function to draw the player
def draw_player(x, y):
    screen.blit(player_image, (x - player_image.get_width() // 2, y - player_image.get_height() // 2))

# Function to start the game
def start_game():
    global game_start_time, target_x, target_y, game_started
    target_x = random.randint(TARGET_RADIUS, WINDOW_WIDTH - TARGET_RADIUS)
    target_y = random.randint(TARGET_RADIUS, WINDOW_HEIGHT - TARGET_RADIUS)
    game_start_time = pygame.time.get_ticks()
    game_started = True

async def main():
    global game_over, score, target_x, target_y, game_started

    running = True
    start_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 100)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.FINGERDOWN and game_started and not game_over:
                # Handle touch events
                touch_pos = event.dict['pos']
                if (touch_pos[0] - target_x) ** 2 + (touch_pos[1] - target_y) ** 2 <= TARGET_RADIUS ** 2:
                    score += 1
                    target_x = random.randint(TARGET_RADIUS, WINDOW_WIDTH - TARGET_RADIUS)
                    target_y = random.randint(TARGET_RADIUS, WINDOW_HEIGHT - TARGET_RADIUS)
            elif event.type == pygame.MOUSEBUTTONDOWN and game_started and not game_over:
                # Handle mouse events
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] - target_x) ** 2 + (mouse_pos[1] - target_y) ** 2 <= TARGET_RADIUS ** 2:
                    score += 1
                    target_x = random.randint(TARGET_RADIUS, WINDOW_WIDTH - TARGET_RADIUS)
                    target_y = random.randint(TARGET_RADIUS, WINDOW_HEIGHT - TARGET_RADIUS)
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                # Start the game
                if start_button_rect.collidepoint(event.pos):
                    start_game()

        # Move the target
        if game_started and not game_over:
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

        # Draw the start button
        if not game_started:
            pygame.draw.rect(screen, WHITE, start_button_rect)
            font = pygame.font.Font(None, 36)
            text = font.render("Click To Start Game", True, BLACK)
            text_rect = text.get_rect(center=(start_button_rect.centerx, start_button_rect.centery))
            screen.blit(text, text_rect)

        # Draw the target
        if game_started:
            draw_target(target_x, target_y)

        # Draw the player
        player_x, player_y = pygame.mouse.get_pos()
        draw_player(player_x, player_y)

        # Display the score and time remaining
        if game_started:
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
        await asyncio.sleep(0)

asyncio.run(main())

# Quit Pygame
pygame.quit()