import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Spaceship settings
SHIP_WIDTH, SHIP_HEIGHT = 50, 40
ship_x = WIDTH // 2 - SHIP_WIDTH // 2
ship_y = HEIGHT - SHIP_HEIGHT - 10
ship_speed = 5

# Bullet settings
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
bullet_speed = 7
bullets = []  # List to keep track of bullets

# Enemy settings
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30
enemy_speed = 2
enemies = []  # List to keep track of enemies

def spawn_enemy():
    """
    Spawns an enemy at a random horizontal position just above the screen.
    """
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = -ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Main game loop
running = True
while running:
    clock.tick(FPS)  # Maintain the game frame rate

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bullet when spacebar is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bullet positioned at the center-top of the spaceship
                bullet_rect = pygame.Rect(
                    ship_x + SHIP_WIDTH // 2 - BULLET_WIDTH // 2,
                    ship_y,
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                )
                bullets.append(bullet_rect)

    # --- Update Game State ---

    # Handle spaceship movement with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_x -= ship_speed
        if ship_x < 0:
            ship_x = 0
    if keys[pygame.K_RIGHT]:
        ship_x += ship_speed
        if ship_x > WIDTH - SHIP_WIDTH:
            ship_x = WIDTH - SHIP_WIDTH

    # Update bullet positions (move them upward)
    for bullet in bullets:
        bullet.y -= bullet_speed
    # Remove bullets that have gone off-screen
    bullets = [b for b in bullets if b.y > -BULLET_HEIGHT]

    # Randomly spawn new enemies (roughly 2 per second)
    if random.randint(1, 30) == 1:
        enemies.append(spawn_enemy())

    # Update enemy positions (move them downward)
    for enemy in enemies:
        enemy.y += enemy_speed
    # Remove enemies that have moved off-screen
    enemies = [e for e in enemies if e.y < HEIGHT]

    # --- Collision Detection ---

    # Create a rectangle for the spaceship for collision detection
    ship_rect = pygame.Rect(ship_x, ship_y, SHIP_WIDTH, SHIP_HEIGHT)

    # Check for collisions between bullets and enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break  # Exit inner loop once collision is detected

    # Check if any enemy collides with the spaceship
    for enemy in enemies:
        if enemy.colliderect(ship_rect):
            print("Game Over!")
            running = False

    # --- Drawing ---
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Draw the spaceship (green rectangle)
    pygame.draw.rect(screen, (0, 255, 0), ship_rect)

    # Draw the bullets (white rectangles)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    # Draw the enemies (red rectangles)
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
