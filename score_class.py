import pygame
import mainBoard

class Score:
    def __init__(self, screen_obj, size = 20, pos = [100, 100], starting_value = 0):
        """int for the game score"""
        self.screen = screen_obj
        """position of score"""
        self.pos = pos
        self.value = starting_value
        self.font = pygame.font.SysFont("monospace", size)
        self.dead = False

    def score(self, amount = 1):
        """current score"""
        self.value += amount

    def render(self):
        """update the score displayed on screen and the lose message if applicable"""
        label = self.font.render(str(self.value), 1, (255, 255, 255))
        lose = self.font.render('YOU LOSE', 1, (255, 0, 0))
        self.screen.blit(label, (self.pos[0], self.pos[1]))
        if(self.dead):
            self.screen.blit(lose, (500, 500))
