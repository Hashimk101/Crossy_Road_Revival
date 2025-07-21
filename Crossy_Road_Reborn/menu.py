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

    
    def showHighScores(self, screen, top_10, font, bg_image):
        """Display the top 10 high scores on the screen"""
    
        # Colors
        TITLE_COLOR = (255, 255, 255)
        SCORE_COLOR = (255, 215, 0)  # Gold color
        RANK_COLOR = (200, 200, 200)  # Light gray
        OVERLAY_COLOR = (0, 0, 0, 180)  # Semi-transparent black overlay
    
        # Draw background image
        screen.blit(bg_image, (0, 0))
    
        # Create semi-transparent overlay for better text readability
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
    
        # Title
        title_text = font.render("HIGH SCORES", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 80))
        screen.blit(title_text, title_rect)
    
        # Display scores
        start_y = 150
        line_height = 45
    
        for i, score in enumerate(top_10[:10]):  # Ensure we only show top 10
            rank = i + 1
        
            # Set all ranks to gold color
            rank_color = (255, 215, 0)  # Gold
            score_color = (255, 215, 0)  # Gold
        
            # Render rank and score
            y_pos = start_y + (i * line_height)
        
            # Rank number
            rank_text = font.render(f"{rank}.", True, rank_color)
            rank_rect = rank_text.get_rect(right=screen.get_width() // 2 - 50, centery=y_pos)
            screen.blit(rank_text, rank_rect)
        
            # Score value
            score_text = font.render(f"{score:,}", True, score_color)  # Format with commas
            score_rect = score_text.get_rect(left=screen.get_width() // 2 + 50, centery=y_pos)
            screen.blit(score_text, score_rect)
    
        # Instructions
        instruction_text = pygame.font.Font(None, 32).render("Press ESC to return to menu", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(instruction_text, instruction_rect)





    
    
