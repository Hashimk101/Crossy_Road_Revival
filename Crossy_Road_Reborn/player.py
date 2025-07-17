from keyword import iskeyword
import pygame

STARTINGX, STARTINGY = 400, 23  # where the player should spawn at the start

class Player:
    def __init__(self):
        self.x = STARTINGX
        self.y = STARTINGY
        self.offset_y = 0
        self.width = 101
        self.height = 60
        self.num_of_frames = 4
        self.animation_index = 0
        self.animation_time = 0
        self.animation_speed = 0.09
        self.isAnimating = False
        self.isKeyPressed = False
        self.direction = 'forward'
        self.forward_sheet = pygame.image.load('../sprites/frog_forward.png').convert_alpha()
        self.side_sheet = pygame.image.load('../sprites/frog_side.png').convert_alpha()
        
        # A list of frames
        self.forward_frames = self.create_frames(self.forward_sheet)
        self.side_frames = self.create_frames(self.side_sheet)
        self.right_side_frames = [pygame.transform.flip(frame, True, False) for frame in self.side_frames]

        # for movement - FIXED VALUES for 8x6 grid
        self.row_height = 100  # 600px / 6 rows = 100px per row
        self.column_width = 100  # 800px / 8 columns = 100px per column
        self.target_x = self.x  # Target position for smooth movement
        self.target_y = self.y
        self.move_speed = 100 / (self.animation_speed * self.num_of_frames)  # pixels per second
        
        # Boundary limits (assuming 800px width screen)
        self.left_boundary = 0
        self.right_boundary = 800 - self.width//2 # 800px - sprite width
        self.top_boundary = 0
        self.bottom_boundary = 600 - self.height  # 600px - sprite height

    def create_frames(self, sprite_sheet):
        frames = []
        for i in range(self.num_of_frames):
            frame_rect = pygame.Rect(i*self.width, 0, self.width, self.height)
            frame = sprite_sheet.subsurface(frame_rect)
            if frame:
                frames.append(frame)
        return frames

    def load_image(self, direction):
        if direction == 'forward':
            return self.forward_frames
        else:
            return self.side_frames

    def animation(self, direction, screen, time):
        if self.isKeyPressed:
            self.isAnimating = True
            self.animation_time += time # delta time from game clock

            if self.animation_time >= self.animation_speed:
                self.animation_index += 1
                self.animation_time = 0
           
            if self.animation_index >= self.num_of_frames:
                self.isAnimating = False
                self.animation_index = 0 # sets to idle immediately
                self.isKeyPressed = False
                self.x = self.target_x
                self.y = self.target_y

            if direction == 'forward' or direction =='backward':
                current_frame = self.forward_frames[self.animation_index]
            elif direction == 'Right_Side':
                current_frame = self.right_side_frames[self.animation_index]
            else:
                current_frame = self.side_frames[self.animation_index]

        else:
            self.animation_index = 0
            self.animation_time = 0
            self.isKeyPressed = False
            self.isAnimating = False

            if direction == 'forward' or direction == 'backward':
                current_frame = self.forward_frames[0]
            elif direction == 'Right_Side':
                current_frame = self.right_side_frames[0]
            else:
                current_frame = self.side_frames[0]

        screen.blit(current_frame, (self.x, self.y))
        if self.animation_index == 0:
            self.isAnimating = False
            return True
        else:
            self.isAnimating = True
            return False

    def movement(self, screen, time):
        if not self.isAnimating:
            dict_of_keys = pygame.key.get_pressed()
            if dict_of_keys[pygame.K_UP]:
                new_y = self.y - self.row_height
                self.isKeyPressed = True
                self.direction = 'forward'
                self.target_y = new_y
                
            elif dict_of_keys[pygame.K_DOWN]:
                new_y = self.y + self.row_height
                if new_y <= self.bottom_boundary:
                    self.isKeyPressed = True
                    self.direction = 'backward'
                    self.target_y = new_y

            elif dict_of_keys[pygame.K_RIGHT]:
                new_x = self.x + self.column_width
                if new_x <= self.right_boundary:
                    self.isKeyPressed = True
                    self.direction = 'Right_Side'
                    self.target_x = new_x

            elif dict_of_keys[pygame.K_LEFT]:
                new_x = self.x - self.column_width
                if new_x >= self.left_boundary:
                    self.isKeyPressed = True
                    self.direction = 'Left_Side'
                    self.target_x = new_x

        self.animation(self.direction, screen, time)
        self.changeLocation(self.direction, time)

    def changeLocation(self, dir, dt):
        if not self.isAnimating:
            return

        move_distance = self.move_speed * dt

        if self.direction == 'forward':
            self.y -= move_distance
    
        elif self.direction == 'backward':
            self.y += move_distance
    
        elif self.direction == 'Right_Side':
            self.x += move_distance
    
        elif self.direction == 'Left_Side':
            self.x -= move_distance



    