import pygame
import mainBoard

class Score:
    def __init__(self, screen_obj, size = 20, pos = [100, 100], starting_value = 0):
        self.screen = screen_obj
        self.pos = pos
        self.value = starting_value
        self.font = pygame.font.SysFont("monospace", size)

    def score(self, amount = 1):
        self.value += amount

    def render(self):
        label = self.font.render(str(self.value), 1, (255, 255, 255))
        self.screen.blit(label, (self.pos[0], self.pos[1]))
