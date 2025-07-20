import pygame

# Constants
STARTING_X, STARTING_Y = 400, 523
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_ROWS = 6
GRID_COLS = 8
SPRITE_WIDTH = 101
SPRITE_HEIGHT = 60
NUM_FRAMES = 4
FRAME_DURATION = 0.10  # Each frame shows for 0.12 seconds
MOVEMENT_DISTANCE = 100  # Player moves 100px per grid step


class Player:
    def __init__(self):
        # Position and movement
        self.x = STARTING_X
        self.y = STARTING_Y
        self.target_x = self.x
        self.target_y = self.y
        
        # Sprite properties
        self.width = SPRITE_WIDTH
        self.height = SPRITE_HEIGHT
        
        # Animation properties
        self.num_frames = NUM_FRAMES
        self.animation_index = 0
        self.animation_time = 0
        self.frame_duration = FRAME_DURATION
        self.is_animating = False
        self.direction = 'forward'
        
        # Movement properties
        self.row_height = MOVEMENT_DISTANCE
        self.column_width = MOVEMENT_DISTANCE
        self.velocity_x = 0
        self.velocity_y = 0
        
        # For frame-rate independent smooth movement
        self.accumulated_movement_x = 0.0
        self.accumulated_movement_y = 0.0
        
        # Calculate velocity for 100px movement over animation duration
        total_animation_time = self.frame_duration * self.num_frames
        self.base_velocity = MOVEMENT_DISTANCE / total_animation_time
        
        # Boundary limits
        self.left_boundary = 0
        self.right_boundary = SCREEN_WIDTH - self.width/2
        self.top_boundary = 0
        self.bottom_boundary = SCREEN_HEIGHT - self.height
        
        # Load and prepare sprites
        self._load_sprites()

    def _load_sprites(self):
        """Load sprite sheets and create animation frames."""
        self.forward_sheet = pygame.image.load('../sprites/frog_forward.png').convert_alpha()
        self.side_sheet = pygame.image.load('../sprites/frog_side.png').convert_alpha()
        
        self.forward_frames = self._create_frames(self.forward_sheet)
        self.side_frames = self._create_frames(self.side_sheet)
        self.right_side_frames = [pygame.transform.flip(frame, True, False) for frame in self.side_frames]

    def _create_frames(self, sprite_sheet):
        """Extract individual frames from a sprite sheet."""
        frames = []
        for i in range(self.num_frames):
            frame_rect = pygame.Rect(i * self.width, 0, self.width, self.height)
            frame = sprite_sheet.subsurface(frame_rect)
            frames.append(frame)
        return frames

    def _get_current_frame(self):
        """Get the current animation frame based on direction."""
        frame_sets = {
            'forward': self.forward_frames,
            'backward': self.forward_frames,
            'Right_Side': self.right_side_frames,
            'Left_Side': self.side_frames
        }
        return frame_sets[self.direction][self.animation_index]

    def _update_animation(self, dt):
        """Update animation state and timing."""
        if not self.is_animating:
            self.animation_index = 0
            self.animation_time = 0
            return

        self.animation_time += dt

        if self.animation_time >= self.frame_duration:
            self.animation_index += 1
            self.animation_time = 0

        if self.animation_index >= self.num_frames:
            self._finish_animation()

    def _finish_animation(self):
        """Complete the current animation and snap to target position."""
        self.is_animating = False
        self.animation_index = 0
        
        # Snap to exact target position
        self.x = self.target_x
        self.y = self.target_y
        
        # Reset movement state
        self.velocity_x = 0
        self.velocity_y = 0
        self.accumulated_movement_x = 0
        self.accumulated_movement_y = 0

    def _update_movement(self, dt):
        """Update position during animation with frame-rate independence."""
        if not self.is_animating:
            return

        # Calculate movement for this frame
        movement_x = self.velocity_x * dt
        movement_y = self.velocity_y * dt
        
        # Accumulate fractional movement for precision
        self.accumulated_movement_x += movement_x
        self.accumulated_movement_y += movement_y
        
        # Apply integer movement
        move_x = int(self.accumulated_movement_x)
        move_y = int(self.accumulated_movement_y)
        
        self.x += move_x
        self.y += move_y
        
        # Keep fractional remainder
        self.accumulated_movement_x -= move_x
        self.accumulated_movement_y -= move_y
        
        # Prevent overshooting target
        self._clamp_to_target()

    def _clamp_to_target(self):
        """Prevent movement from overshooting the target position."""
        if self.velocity_x > 0 and self.x >= self.target_x:
            self.x = self.target_x
        elif self.velocity_x < 0 and self.x <= self.target_x:
            self.x = self.target_x
            
        if self.velocity_y > 0 and self.y >= self.target_y:
            self.y = self.target_y
        elif self.velocity_y < 0 and self.y <= self.target_y:
            self.y = self.target_y

    def _can_move_to(self, target_x, target_y):
        """Check if the target position is within boundaries."""
        return (self.left_boundary <= target_x <= self.right_boundary and
                self.top_boundary <= target_y <= self.bottom_boundary)

    def _start_movement(self, direction, target_x, target_y, vel_x, vel_y):
        """Initialize movement in a given direction."""
        if self._can_move_to(target_x, target_y):
            self.is_animating = True
            self.direction = direction
            self.target_x = target_x
            self.target_y = target_y
            self.velocity_x = vel_x
            self.velocity_y = vel_y
            return True
        return False

    def handle_input(self):
        """Process keyboard input for movement."""
        if self.is_animating:
            return

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self._start_movement('forward', 
                               self.x, self.y - self.row_height,
                               0, -self.base_velocity)
                               
        elif keys[pygame.K_DOWN]:
            self._start_movement('backward',
                               self.x, self.y + self.row_height,
                               0, self.base_velocity)
                               
        elif keys[pygame.K_RIGHT]:
            self._start_movement('Right_Side',
                               self.x + self.column_width, self.y,
                               self.base_velocity, 0)
                               
        elif keys[pygame.K_LEFT]:
            self._start_movement('Left_Side',
                               self.x - self.column_width, self.y,
                               -self.base_velocity, 0)

    def update(self, dt):
        """Update player state - call this every frame."""
        self.handle_input()
        self._update_animation(dt)
        self._update_movement(dt)

    def draw(self, screen):
        """Draw the player sprite to the screen."""
        current_frame = self._get_current_frame()
        screen.blit(current_frame, (self.x, self.y))

    def is_movement_finished(self):
        """Check if the current movement animation is complete."""
        return not self.is_animating

    def move_down_const(self, move_speed,dt):
        self.y += (move_speed + 10) *dt
        self.target_y += (move_speed + 10) *dt
