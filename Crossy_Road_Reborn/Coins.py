from pickle import TRUE
import pygame
import random
import time

class COINS(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.coins = 0
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.active = True  # Bool to turn coin on/off
        
        # Load and setup sprite sheet
        self.sprite_sheet = pygame.image.load("../sprites/rings.png").convert_alpha()
        self.numframes = 4
        self.curr_frame = 0
        self.animationspeed = 0.2  # in seconds
        self.last_update = time.time()
        
        # Extract individual frames from sprite sheet
        self.frames = []
        frame_width = self.sprite_sheet.get_width() // self.numframes
        frame_height = self.sprite_sheet.get_height()
        
        for i in range(self.numframes):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            # Scale frame to desired size
            frame = pygame.transform.scale(frame, (self.width, self.height))
            self.frames.append(frame)
        
        # Set initial image and rect
        self.image = self.frames[self.curr_frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Collision detection
        self.collected = False
    
    def update(self):
        """Update animation and coin state"""
        if not self.active or self.collected:
            self.kill()  # Remove from sprite group
            return
        
        # Update animation
        current_time = time.time()
        if current_time - self.last_update >= self.animationspeed:
            self.curr_frame = (self.curr_frame + 1) % self.numframes
            self.image = self.frames[self.curr_frame]
            self.last_update = current_time
    
    def collect(self):
        """Called when coin is collected"""
        if not self.collected and self.active:
            self.collected = True
            return True  # Return True if coin was successfully collected
        return False
    
    def toggle_active(self):
        """Toggle coin on/off"""
        self.active = not self.active
    
    def set_active(self, active):
        """Set coin active state"""
        self.active = active


def create_coin_sprites(map_width, map_height, grid_size=100, coins_per_10_rows=3, y_offset=0):
    """
    Create coin sprites positioned randomly on the map
    
    Args:
        map_width: Width of the map in pixels
        map_height: Height of the map in pixels
        grid_size: Size of each grid cell (default 100x100)
        coins_per_10_rows: Number of coins to place per 10 rows (3-4 range)
        y_offset: Starting y-position offset (e.g., -200 to start above screen)
    
    Returns:
        pygame.sprite.Group: Group containing all coin sprites
    """
    coin_group = pygame.sprite.Group()
    
    # Calculate grid dimensions
    grid_cols = map_width // grid_size
    grid_rows = map_height // grid_size
    
    # Calculate how many coins to place
    rows_groups = grid_rows // 10  # Number of 10-row groups
    remaining_rows = grid_rows % 10
    
    total_coins = 0
    
    # Place coins for complete 10-row groups
    for group in range(rows_groups):
        num_coins = random.randint(coins_per_10_rows, coins_per_10_rows + 1)  # 3 or 4 coins
        total_coins += num_coins
        
        for _ in range(num_coins):
            # Random position within this 10-row group
            col = random.randint(0, grid_cols - 1)
            row = random.randint(group * 10, (group + 1) * 10 - 1)
            
            # Convert grid position to pixel position (center of grid cell)
            x = col * grid_size + (grid_size - 50) // 2  # Center coin in grid
            y = row * grid_size + (grid_size - 50) // 2 + y_offset
            
            coin = COINS(x, y)
            coin_group.add(coin)
    
    # Place coins for remaining rows (if any)
    if remaining_rows > 0:
        # Scale down coins for partial group
        num_coins = int((remaining_rows / 10) * coins_per_10_rows)
        num_coins = max(1, num_coins)  # At least 1 coin
        
        for _ in range(num_coins):
            col = random.randint(0, grid_cols - 1)
            row = random.randint(rows_groups * 10, grid_rows - 1)
            
            x = col * grid_size + (grid_size - 50) // 2
            y = row * grid_size + (grid_size - 50) // 2 + y_offset
            
            coin = COINS(x, y)
            coin_group.add(coin)
    
    return coin_group


def toggle_all_coins(coin_group, active_state=None):
    """
    Toggle all coins in a group on/off
    
    Args:
        coin_group: pygame.sprite.Group containing coins
        active_state: If None, toggle each coin. If bool, set all coins to that state
    """
    for coin in coin_group:
        if active_state is None:
            coin.toggle_active()
        else:
            coin.set_active(active_state)


def move_ground(sprite_group, dt, move_speed):
    """
    keeps moving ground down by move speed, doesnt return anything as python will 
    pass it by reference
    """
    for sprite in sprite_group:
        sprite.rect.y += move_speed * dt


def checkCollisionWithPlayer(player, coin_group):

    hasCollided = False

    set_of_collided = pygame.sprite.spritecollide(player, coin_group, False)
    for coin in set_of_collided:
        if coin.collect():
            hasCollided = True
            coin_group.remove(coin)  # Remove coin from group after collection


    return hasCollided

# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()
    
    # Create coins for a 1200x800 map, starting 200px above the screen
    coins = create_coin_sprites(1200, 800, grid_size=100, coins_per_10_rows=3, y_offset=-200)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Toggle all coins on space press
                    toggle_all_coins(coins)
        
        # Update and draw
        coins.update()
        screen.fill((0, 0, 0))
        coins.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()