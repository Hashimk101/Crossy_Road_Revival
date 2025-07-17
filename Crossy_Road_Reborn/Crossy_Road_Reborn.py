import pygame
import sys
import random
import time
import player

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600;
FPS = 60

# setting up basic stuff
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

main_font = pygame.font.Font('../FONT/VIDEOPHREAK.ttf', 20)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Road Reborn")
curr_player = player.Player()
# Load the player sprite
player_sprite = curr_player.load_image('forward')

isGameRunning = True
while isGameRunning:
    dt = clock.tick(FPS) / 1000  # dt in seconds (float)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False
            sys.exit()
    screen.fill((30, 70, 100))
    curr_player.movement(screen, dt)
    print(f"Player position: ({curr_player.x}, {curr_player.y})")
    pygame.display.flip()
    clock.tick(FPS)  # Limit to 60 FPS

pygame.quit()