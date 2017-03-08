import pygame

class Score():
    def __init__(self, size = 20, pos = [100, 100], starting_value = 0):
        self.pos = pos
        self.value = starting_value
        self.font = pygame.font.SysFont("monospace", size)

    def score(self, amount = 1):
        self.value += amount

    def render(self):
        label = self.font.render(str(self.value), 1, (255, 255, 255))
        screen.blit(label, (pos[1], pos[2]))
