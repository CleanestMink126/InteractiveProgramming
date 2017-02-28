""" Experiment with face detection and image filtering using OpenCV """
import shipClass

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
        black = 0, 0, 0
        screen = pygame.display.set_mode(size)
        # ball = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 10, 0)
        mainShip = shipClass.Ship()
        mainShip.speed = [8,5]
        shipImage = pygame.image.load(os.path.join('rocket.png'))
        shipImage = pygame.transform.scale(shipImage, (50, 50))
        shipImage = pygame.transform.rotate(shipImage, -45)
        ship = shipImage.copy()
        shiprect = ship.get_rect()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    ship = rot_center(shipImage, 45)
                    shiprect = ship.get_rect()
                    shiprect = shiprect.move(mainShip.pos[0], mainShip.pos[1])
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    ship = rot_center(shipImage, -45)
                    shiprect = ship.get_rect()
                    shiprect = shiprect.move(mainShip.pos[0], mainShip.pos[1])
            shiprect = shiprect.move(mainShip.speed[0], mainShip.speed[1])
            mainShip.pos[0] += mainShip.speed[0]
            mainShip.pos[1] += mainShip.speed[1]
            if shiprect.left < 0 or shiprect.right > width:
                mainShip.speed[0] = -mainShip.speed[0]
            if shiprect.top < 0 or shiprect.bottom > height:
                mainShip.speed[1] = -mainShip.speed[1]
            screen.fill(black)
            screen.blit(ship, shiprect)
            pygame.display.flip()
            pygame.time.wait(20)
        pygame.display.quit()
        pygame.quit()
        sys.exit()


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


if __name__ == '__main__':
    board = BoardInit()
