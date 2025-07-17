import random
from tkinter.tix import Tree
import pygame

# add one more row than the actual visible size for smoother movement if needed later
list_of_grounds = ['road', 'tiles', 'road', 'road', 'tiles']
list_of_plants = ['None', 'None', 'None', 'None', 'None', 'None', 'None', 'trees', 'bushes', 'None', 'None', 'None', 'None','None', 'None', 'None']

def ground_filler():
    '''
        Makes the initial 8 rows of ground
    '''
    ground_rows = []
    for i in range(8):
        choice = random.choice(list_of_grounds)  # get a random ground type
        ground_rows.append(choice)
    return ground_rows

def renew_ground(ground_rows):
    '''
        Renews the top row each time it is called.
        Shifts all rows down, drops the bottom one, and adds a new one on top.
    '''
    new_ground = []
    choice = random.choice(list_of_grounds)
    new_ground.append(choice)
    for i in range(1, 8):
        new_ground.append(ground_rows[i])
    return new_ground

def make_objects():
    obj_list = []
    for i in range(48):  # 8 columns × 6 rows
        choice = random.choices(['trees', 'bushes', 'None'], weights=[1, 1, 15], k=1)[0]
        obj_list.append(choice)
    return obj_list


def renew_objects(obj_list):
    new_list = []
    for i in range(8):
        choice = random.choices(['trees', 'bushes', 'None'], weights=[1, 1, 15], k=1)[0]
        new_list.append(choice)
    for i in range(8, 48):
        new_list.append(obj_list[i])
    return new_list


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0): # Fixed double asterisks
        super().__init__() # Initialize the base Sprite class
        self.image = image
        self.rect = self.image.get_rect() # Get the bounding rectangle of the image
        self.rect.topleft = (x, y) # Set the initial position (can be updated later)

def create_sprites():
    """
    Loads images and converts them into instances of the GameObject sprite class.
    """
    tree_img = pygame.image.load('../sprites/Tree.png').convert_alpha()
    bush_img = pygame.image.load('../sprites/Bush.png').convert_alpha()
   
    # You can set their initial positions here, or leave them at (0,0) and adjust later.
    tree_sprite = GameObject(tree_img)
    bush_sprite = GameObject(bush_img)
    return tree_sprite, bush_sprite

def grid_to_pixel(col, row, grid_size=100):
    """
    Converts grid coordinates to pixel coordinates.
    """
    x = col * grid_size
    y = row * grid_size
    return x, y

def create_sprite_grid(obj_list, tree_sprite, bush_sprite, grid_size=100):
    """
    Creates a sprite group with sprites positioned based on the object list.
    obj_list: 1D array of 48 elements (8 columns x 6 rows)
    Returns a pygame sprite group with positioned sprites.
    """
    sprite_group = pygame.sprite.Group()
    
    for i, obj_type in enumerate(obj_list):
        if obj_type != 'None':
            # Calculate grid position from 1D index
            col = i % 8  # Column (0-7)
            row = i // 8  # Row (0-5)
            
            # Convert grid position to pixel coordinates
            x, y = grid_to_pixel(col, row, grid_size)
            
            # Create appropriate sprite based on object type
            if obj_type == 'trees':
                # Create a new tree sprite at this position
                new_sprite = GameObject(tree_sprite.image, x, y)
                sprite_group.add(new_sprite)
            elif obj_type == 'bushes':
                # Create a new bush sprite at this position
                new_sprite = GameObject(bush_sprite.image, x, y)
                sprite_group.add(new_sprite)
    
    return sprite_group

def shift_sprites_down(sprite_group, grid_size=100):
    """
    Shifts all existing sprites down by one row (for Crossy Road style movement).
    Removes sprites that go off the bottom of the screen.
    """
    sprites_to_remove = []
    
    for sprite in sprite_group:
        # Move sprite down by one grid cell
        sprite.rect.y += grid_size
        
        # Remove sprites that have moved off the bottom (row 6 and beyond)
        if sprite.rect.y >= 6 * grid_size:
            sprites_to_remove.append(sprite)
    
    # Remove off-screen sprites
    for sprite in sprites_to_remove:
        sprite_group.remove(sprite)

def add_new_top_row(sprite_group, obj_list, tree_sprite, bush_sprite, grid_size=100):
    """
    Adds sprites for the new top row only (first 8 elements of obj_list).
    Used after calling renew_objects() in a Crossy Road style game.
    """
    # Only process the first 8 elements (top row)
    for i in range(8):
        obj_type = obj_list[i]
        if obj_type != 'None':
            col = i % 8  # Column (0-7)
            row = 0      # Always top row
            x, y = grid_to_pixel(col, row, grid_size)
            
            if obj_type == 'trees':
                new_sprite = GameObject(tree_sprite.image, x, y)
                sprite_group.add(new_sprite)
            elif obj_type == 'bushes':
                new_sprite = GameObject(bush_sprite.image, x, y)
                sprite_group.add(new_sprite)

def update_sprites_crossy_road(sprite_group, obj_list, tree_sprite, bush_sprite, grid_size=100):
    """
    Updates sprites for Crossy Road style movement:
    1. Shifts all existing sprites down by one row
    2. Adds new sprites for the top row only
    """
    shift_sprites_down(sprite_group, grid_size)
    add_new_top_row(sprite_group, obj_list, tree_sprite, bush_sprite, grid_size)


class Trees:
    def __init__(self, image, x=0, y=0): # Fixed double asterisks
        super().__init__() # Initialize the base Sprite class
        self.image = image
        self.rect = self.image.get_rect() # Get the bounding rectangle of the image
        self.rect.topleft = (x, y) # Set the initial position (can be updated later)


def create_ground_sprite():
    road = pygame.image.load('../sprites/road.png').convert_alpha()
    tiles = pygame.image.load('../sprites/tiles.png').convert_alpha()
   
    # You can set their initial positions here, or leave them at (0,0) and adjust later.
    road_sprite = GameObject(road)
    tile_sprite = GameObject(tiles)
    return road_sprite, tile_sprite


def create_background(ground_rows, road_sprite, tiles_sprite):
    '''
        creates a 8 row ground sprite group
        for a small grid like this, recreating the whole sprite group again
        and again shouldnt be that problematic ig
    '''
    sprite_group = pygame.sprite.Group()
    
    for index, ground in enumerate(ground_rows):
        y_part = index * 100

        if ground == 'road':
            curr_sprite = Trees(road_sprite, 0, y_part)
            sprite_group.add(curr_sprite)
        elif ground == 'tiles':
            curr_sprite = Trees(tiles_sprite, 0, y_part)
            sprite_group.add(curr_sprite)

    return sprite_group