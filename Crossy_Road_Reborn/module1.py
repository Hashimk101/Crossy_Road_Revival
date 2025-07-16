import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move the Box")

# Box settings
box_size = 50
box_x = width // 2 - box_size // 2
box_y = height // 2 - box_size // 2
box_speed = 5
box_color = (0, 128, 255)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and box_x > 0:
        box_x -= box_speed
    if keys[pygame.K_RIGHT] and box_x < width - box_size:
        box_x += box_speed
    if keys[pygame.K_UP] and box_y > 0:
        box_y -= box_speed
    if keys[pygame.K_DOWN] and box_y < height - box_size:
        box_y += box_speed
    
    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_size, box_size))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()