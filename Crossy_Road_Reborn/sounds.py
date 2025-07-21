import pygame

class Sounds:
    def __init__(self):
        # Music tracks
        self.menu_sound = '../Music/startup.ogg'
        self.game_sound = '../Music/main_game.ogg'
        # Sound effects
        self.coin_sound = pygame.mixer.Sound('../Sound/coin_collect.ogg')
        self.game_oversound = pygame.mixer.Sound('../Sound/game_over.wav')
        self.jump_sound = pygame.mixer.Sound('../Sound/jump.wav')
        
        # Track what's currently playing
        self.current_music = None
        
    def playMenu(self):
        # Only load and play if not already playing menu music
        if self.current_music != 'menu':
            pygame.mixer.music.load(self.menu_sound)
            pygame.mixer.music.play(-1)  # Loop forever
            self.current_music = 'menu'
        
    def playGame(self):
        # Only load and play if not already playing game music
        if self.current_music != 'game':
            pygame.mixer.music.load(self.game_sound)
            pygame.mixer.music.play(-1)
            self.current_music = 'game'
        
    def playCoinCollect(self):
        self.coin_sound.play()
        
    def playJump(self):
        self.jump_sound.play()
        
    def playGameOver(self):
        self.game_oversound.play()
        
    def stopMusic(self):
        pygame.mixer.music.stop()
        self.current_music = None