""" Experiment with face detection and image filtering using OpenCV """
# import shipClass

import os
import sys
import pygame
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


class BoardInit:
    def __init__(self):
        pygame.init()

        size = width, height = 1000, 1000
        speed = [2, 2]
        black = 0, 0, 0

        screen = pygame.display.set_mode(size)
        ball = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 10, 0)

        ship = pygame.image.load(os.path.join('rocket.png'))
        shiprect = ship.get_rect()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return
                elif event.type == pygame.MOUSEBUTTONUP:
                    return
            #ball = ball.move(speed)
            shiprect = shiprect.move(speed)
            if ball.left < 0 or ball.right > width:
                speed[0] = -speed[0]
            if ball.top < 0 or ball.bottom > height:
                speed[1] = -speed[1]

            screen.fill(black)

            screen.blit(ship, shiprect)
            #pygame.draw.circle(screen, (255, 0, 0), (10, 10), 10, 0)
            pygame.display.flip()
        pygame.display.quit()
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    board = BoardInit()
