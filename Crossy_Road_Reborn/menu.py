import pygame

def showBackground(screen, image):
    screen.blit(image, (0, 0))


class Menu:

    def __init__(self, screen, font):
         # Render text surfaces
        self.color = (255, 215, 0) 
        self.title_text = font.render("Crossy Road Reborn", True, self.color)
        self.play_text = font.render("Play Game", True, self.color)
        self.high_scores_text = font.render("High Scores", True, self.color)
        self.quit_text = font.render("Quit Game", True, self.color)
        screen_width = 800
        screen_height = 600
    
        # Title (top-center)
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 80))
        
        # Menu options (centered vertically)
        self.play_rect = self.play_text.get_rect(center=(screen_width // 2, 280))

        self.high_scores_rect = self.high_scores_text.get_rect(center=(screen_width // 2, 350))

        self.quit_rect = self.quit_text.get_rect(center=(screen_width // 2, 420))


    def showMenu(self, screen, font, image):
        
        showBackground(screen, image)
        # Center text horizontally
        
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.play_text, self.play_rect)
        screen.blit(self.high_scores_text, self.high_scores_rect)
        screen.blit(self.quit_text, self.quit_rect)

    



    
    
