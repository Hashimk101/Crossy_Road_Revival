import pygame
import sys
import player
import Ground
import Coins
import scores

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
MOVESPEED = 32

# Grid constants
GRID_ROWS = 6
GRID_COLS = 8
GRID_CELL_WIDTH = SCREEN_WIDTH // GRID_COLS  # 100px
GRID_CELL_HEIGHT = SCREEN_HEIGHT // GRID_ROWS  # 100px

# Colors
BACKGROUND_COLOR = (30, 70, 100)
GRID_LINE_COLOR = (100, 100, 100)
GRID_LINE_WIDTH = 1

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Road Reborn")

# Game objects
curr_player = player.Player()
ground_rows = Ground.ground_filler()
road_sprite, tiles_sprite = Ground.create_ground_sprite()
tree_sprite, bush_sprite = Ground.create_sprites()

sprite_group1 = Ground.create_background(ground_rows, road_sprite, tiles_sprite, -4400)
ground_rows = Ground.ground_filler()
sprite_group2 = Ground.create_background(ground_rows, road_sprite, tiles_sprite, -9400)

obj_list = Ground.make_objects()
objects_group1 = Ground.create_sprite_grid(obj_list, tree_sprite, bush_sprite,-200)
obj_list = Ground.make_objects()
objects_group2 = Ground.create_sprite_grid(obj_list, tree_sprite, bush_sprite,-1000)

coins = Coins.create_coin_sprites(800, 600, 100, 10, y_offset=-500)

scores_system = scores.Scores()

for obj in objects_group1:
        print(obj.rect.x, obj.rect.y)
for obj in objects_group2:
        print(obj.rect.x, obj.rect.y)

def draw_grid(surface):
    """Draw grid lines on the screen."""
    # Draw vertical lines
    for col in range(GRID_COLS + 1):
        x = col * GRID_CELL_WIDTH
        pygame.draw.line(surface, GRID_LINE_COLOR, (x, 0), (x, SCREEN_HEIGHT), GRID_LINE_WIDTH)
    
    # Draw horizontal lines
    for row in range(GRID_ROWS + 1):
        y = row * GRID_CELL_HEIGHT
        pygame.draw.line(surface, GRID_LINE_COLOR, (0, y), (SCREEN_WIDTH, y), GRID_LINE_WIDTH)

def get_topmost_coin_y(coin_group):
    """Get the y position of the topmost coin in the group"""
    if not coin_group.sprites():
        return float('inf')  # Return a large number if no coins exist
    
    return min(coin.rect.top for coin in coin_group.sprites())

# Game loop
isGameRunning = True
while isGameRunning:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False
            pygame.quit()
            sys.exit()
    
    # Clear screen
    screen.fill(BACKGROUND_COLOR)
    sprite_group1.draw(screen)
    sprite_group2.draw(screen)
    Ground.move_ground(sprite_group1, dt, MOVESPEED)
    Ground.move_ground(sprite_group2, dt, MOVESPEED)
    curr_player.move_down_const(MOVESPEED, dt)
    Ground.reposition_objects(objects_group1, tree_sprite, bush_sprite)
    Ground.reposition_objects(objects_group2, tree_sprite, bush_sprite)
    Ground.move_objects_down(objects_group1, MOVESPEED, dt)
    Ground.move_objects_down(objects_group2, MOVESPEED, dt)
    
    # Update coins
    coins.update()
    coins.draw(screen)
    Coins.move_ground(coins, dt, MOVESPEED)

    # print(f"score: {scores_system.getScore()}")
    # check collision between player and coins
    if Coins.checkCollisionWithPlayer(curr_player, coins):
        scores_system.add_score(5)
    scores_system.add_constant_score(dt)
    
    
    # Check if topmost coin has moved below screen and recreate coins if needed
    topmost_coin_y = get_topmost_coin_y(coins)
    if topmost_coin_y > SCREEN_HEIGHT:  # 600px
        # Clear existing coins
        coins.empty()
        # Create new coins starting at -500px
        coins = Coins.create_coin_sprites(SCREEN_WIDTH, SCREEN_HEIGHT, 100, 3, y_offset=-600)
    
    # Check if either the first or last sprite in group1 is within the extended range
    if (objects_group1.sprites() and 
        (-200 <= objects_group1.sprites()[0].rect.top <= 800 or 
         -200 <= objects_group1.sprites()[-1].rect.top <= 800)):
        objects_group1.draw(screen)
    # Check if either the first or last sprite in group2 is within the extended range
    if (objects_group2.sprites() and 
        (-200 <= objects_group2.sprites()[0].rect.top <= 800 or 
         -200 <= objects_group2.sprites()[-1].rect.top <= 800)):
        objects_group2.draw(screen)
    
    # Update and draw player
    curr_player.update(dt, objects_group1, objects_group2)
    curr_player.draw(screen)
    
    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()