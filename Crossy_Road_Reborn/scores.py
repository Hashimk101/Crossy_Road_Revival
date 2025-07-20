import pygame
import time

class Scores:
    def __init__(self):
        self.scores = 0
        self.stop = False
        self.current_animation = 0
        self.animation_time = 1.5

    def add_score(self, points):
        self.scores += points
    
    def add_constant_score(self, dt):
        if self.stop:
           return
       
        if self.current_animation < self.animation_time:
            self.current_animation += dt

        else:
            self.current_animation = 0
            self.scores += 1

    def getScore(self):
        return self.scores

    def reset_score(self):
        self.scores = 0
        self.stop = True
        self.current_animation = 0

    def addtoFile(self):
        scores_file = open("../text_files/scores.txt", "a")
        scores_file.write(str(self.scores) + "\n")

    def readfromfile(self):
        with open("../text_files/scores.txt", "r") as scores_file:
            scores = scores_file.readlines()
            # Convert to integers, remove empty lines, and sort descending
            scores = [int(score.strip()) for score in scores if score.strip()]
            top_10 = sorted(scores, reverse=True)[:10]
        return top_10