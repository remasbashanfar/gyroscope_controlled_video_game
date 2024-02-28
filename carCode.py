import pygame
import random

# Initialize Pygame and set up the display window
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define paths for images
player_image_path = 'car (1).png'
fire_image_path = 'fire.png'
enemy_image_paths = [f'car ({i}).png' for i in range(2, 8)]
road_image_path = 'road.png'

# Load images
road_background = pygame.image.load(road_image_path).convert()
player_image = pygame.image.load(player_image_path).convert_alpha()
fire_image = pygame.image.load(fire_image_path).convert_alpha()  # Load the fire image here
# Scale the fire image to appropriate size if needed
fire_image = pygame.transform.scale(fire_image, (100, 100))

# Function to scale an image while maintaining aspect ratio
def scale_image(img, width):
    # Calculate the factor to maintain aspect ratio
    height = int(img.get_height() * width / img.get_width())
    return pygame.transform.scale(img, (width, height))

# Function to load and scale a random enemy car image
def load_and_scale_random_enemy_image():
    enemy_img = scale_image(pygame.image.load(random.choice(enemy_image_paths)).convert_alpha(), 100)
    return enemy_img

# Scale background and player image
road_background = pygame.transform.scale(road_background, (screen_width, screen_height))
player_image = scale_image(player_image, 100)

# Initialize enemy image
enemy_image = load_and_scale_random_enemy_image()

player_pos = [screen_width // 2 - 25, screen_height - 120]  # Center the player car
enemy_pos = [random.randint(0, screen_width - 50), -100]
score = 0
font = pygame.font.SysFont(None, 35)

# def player_collides_with_enemy(player_pos, enemy_pos):
#     player_rect = player_image.get_rect(topleft=player_pos)
#     enemy_rect = enemy_image.get_rect(topleft=enemy_pos)
    
#     # Shrink the rectangles for a more accurate collision detection
#     collision_tolerance = 10  # Amount to shrink the rectangles by on each side
#     player_rect = player_rect.inflate(-collision_tolerance, -collision_tolerance)
#     enemy_rect = enemy_rect.inflate(-collision_tolerance, -collision_tolerance)

#     return player_rect.colliderect(enemy_rect)
def player_collides_with_enemy(player_pos, enemy_pos):
    # Define a smaller hitbox for more accurate collision detection
    # The hitbox is a rectangle that is slightly smaller than the image
    hitbox_offset = 60  

    player_hitbox = player_image.get_rect(topleft=player_pos).inflate(-hitbox_offset, -hitbox_offset)
    enemy_hitbox = enemy_image.get_rect(topleft=enemy_pos).inflate(-hitbox_offset, -hitbox_offset)

    return player_hitbox.colliderect(enemy_hitbox)

# Define the game loop
running = True
crash = False
while running:
    # Check for game events (like quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Handle player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5  # Move left
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - 50:
        player_pos[0] += 5  # Move right

    # Update enemy position
    enemy_pos[1] += 7  # Enemy car speed
    if enemy_pos[1] > screen_height:
        enemy_pos[0] = random.randint(0, screen_width - 50)
        enemy_pos[1] = -100
        enemy_image = load_and_scale_random_enemy_image()  # Load and scale a new random enemy car image
        score += 1  # Increase score as the player avoids an enemy

    # Draw everything: the background, player, enemy, and score
    screen.blit(road_background, (0, 0))
    screen.blit(player_image, player_pos)
    screen.blit(enemy_image, enemy_pos)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    score_text_rect = score_text.get_rect(center=(screen_width // 2, 10))
    screen.blit(score_text, score_text_rect)

    # Check for collisions
    if player_collides_with_enemy(player_pos, enemy_pos) and not crash:
        crash = True
        crash_pos = player_pos  # Store the position where the crash occurred

    if crash:
        screen.blit(fire_image, crash_pos)  # Draw the fire image at the crash position
        pygame.display.flip()  # Update the display to show the fire effect
        pygame.time.delay(500)  # Keep the fire effect for 500 milliseconds
        break  # Exit the game loop after showing the fire effect


    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.delay(30)

# End the game and close the window
pygame.quit()