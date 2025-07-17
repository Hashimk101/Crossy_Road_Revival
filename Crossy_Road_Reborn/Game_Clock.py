import pygame

class game_clock:
    def __init__(self, clock):
        self.clock = clock
        self.starting_time = pygame.time.get_ticks()/1000 #in seconds
        self.current_time = self.starting_time # in seconds
        self.elapsed_time = 0


    def update_time(self):
        self.current_time = pygame.time.get_ticks()/1000
        self.elapsed_time = self.current_time - self.starting_time

    def get_elapsed_time(self):
        return self.elapsed_time