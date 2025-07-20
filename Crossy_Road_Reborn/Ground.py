import random
import pygame
from pygame import sprite

# add one more row than the actual visible size for smoother movement if needed later
list_of_grounds = ['road', 'tiles']
list_of_plants = ['None', 'None', 'None', 'None', 'None', 'None', 'None', 'trees', 'bushes', 'None', 'None', 'None', 'None','None', 'None', 'None']

def ground_filler():
    '''
        Makes the initial 50 rows of ground
    '''
    ground_rows = []
    for i in range(50):
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

def create_sprite_grid(obj_list, tree_sprite, bush_sprite, start_y=0, grid_size=100):
   """
   Creates a sprite group with sprites positioned based on the object list.
   obj_list: 1D array of 400 elements (8 columns x 50 rows)
   start_y: Y position offset where sprites should start being positioned
   Returns a pygame sprite group with positioned sprites.
   """
   sprite_group = pygame.sprite.Group()
   
   for i, obj_type in enumerate(obj_list):
       if obj_type != 'None':
           # Calculate grid position from 1D index
           col = i % 8   # Column (0-7)
           row = i // 8  # Row (0-49)
           
           # Convert grid position to pixel coordinates
           x, y = grid_to_pixel(col, row, grid_size)
           
           # Apply the Y offset
           y += start_y
           
           # Create appropriate sprite based on object type
           if obj_type == 'trees':
               new_sprite = GameObject(tree_sprite.image, x, y)
               sprite_group.add(new_sprite)
           elif obj_type == 'bushes':
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


def move_objects_down(object_group, move_speed, dt):
    for sprite in object_group:
        sprite.rect.y += move_speed * dt


def reposition_objects(object_group, tree_sprite, bush_sprite):
    '''
    as soon as the first part goes completely out of the window, it reappears higher 
    than the second one, so basically they swapped places
    '''
    if object_group.sprites():  # Make sure group isn't empty
        # Convert to list and get first sprite (index 0)
        sprites_list = object_group.sprites()
        first_sprite = sprites_list[0]
        
        # If the first sprite has moved past 600px
        if first_sprite.rect.y > 600:
            # Clear the old group and create new objects
            object_group.empty()
            obj_list = make_objects()
            new_group = create_sprite_grid(obj_list, tree_sprite, bush_sprite, -1000)
            object_group.add(new_group.sprites())
    
    return object_group




class Grounds(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def create_ground_sprite():
    road = pygame.image.load('../sprites/road.png').convert_alpha()
    tiles = pygame.image.load('../sprites/tiles.png').convert_alpha()
    
    # Resize each one to 800px wide, keep height the same
    road = pygame.transform.scale(road, (800, 200))
    tiles = pygame.transform.scale(tiles, (800, 100))
    
    road_sprite = Grounds(road)
    tile_sprite = Grounds(tiles)
    return road_sprite, tile_sprite

def create_background(ground_rows, road_sprite, tiles_sprite, y_position):
    sprite_group = pygame.sprite.Group()
    
    
    for ground in ground_rows:
        if ground == 'road':
            sprite_group.add(Grounds(road_sprite.image, 0, y_position))
            y_position += 200
        elif ground == 'tiles':
            sprite_group.add(Grounds(tiles_sprite.image, 0, y_position))
            y_position += 100
    
    return sprite_group



def move_ground(sprite_group, dt, move_speed):
    """
    keeps moving ground down by move speed, doesnt return anything as python will 
    pass it by reference
    """

    for sprite in sprite_group:
        sprite.rect.y += move_speed * dt
    
    

    


