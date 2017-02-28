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
    def rotShip(self, myangle):
        self.mainShip.rotatecw(angle=myangle)
        self.ship = rot_center(self.shipImage, self.mainShip.get_angle_from_vert())
        self.shiprect = self.ship.get_rect()
        self.shiprect = self.shiprect.move(self.mainShip.pos[0], self.mainShip.pos[1])

    def accelerate(self):
        self.mainShip.speed[0] -= (self.mainShip.direct[0])
        self.mainShip.speed[1] -= (self.mainShip.direct[1])

    def moveShip(self):
        myTime = self.detTime()
        xc = self.mainShip.speed[0]
        yc = self.mainShip.speed[1]
        self.shiprect = self.shiprect.move(int(xc * myTime), int(yc * myTime))
        self.mainShip.pos[0] += int(xc * myTime)
        self.mainShip.pos[1] += int(yc * myTime)

    def gravity(self):
        distance = self.distanceCent()
        self.mainShip.speed[0] -= ((self.mainShip.pos[0]-self.center[0])/distance * .3)
        self.mainShip.speed[1] -= ((self.mainShip.pos[1]-self.center[1])/distance * .3)

    def distanceCent(self):
        return ((self.mainShip.pos[0]-self.center[0]) ** 2 + (self.mainShip.pos[1] - self.center[1]) ** 2) ** .5

    def detTime(self):
        distance = self.distanceCent()
        print(distance)
        return distance / (distance + 500)

    def checkBounds(self):
        if self.shiprect.left < 0 or self.shiprect.right > self.width:
            self.mainShip.speed[0] = 0
        if self.shiprect.top < 0 or self.shiprect.bottom > self.height:
            self.mainShip.speed[1] = 0

    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1800, 1000
        black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        # ball = pygame.draw.circle(self.screen, (255, 0, 0), (10, 10), 10, 0)
        self.mainShip = shipClass.Ship(direct = [0,1], speed = [0,0], pos = [500,500])
        self.center = [self.width/2, self.height/2]

        self.shipImage = pygame.image.load(os.path.join('rocket.png'))
        self.shipImage = pygame.transform.scale(self.shipImage, (50, 50))
        self.shipImage = pygame.transform.rotate(self.shipImage, -45)
        self.ship = self.shipImage.copy()
        self.shiprect = self.ship.get_rect()
        self.shiprect = self.shiprect.move(self.mainShip.pos)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_LEFT]:
                self.rotShip(10)
            if keys[pygame.K_RIGHT]:
                self.rotShip(-10)
            if keys[pygame.K_SPACE]:
                self.accelerate()
            self.moveShip()
            #self.checkBounds()
            self.gravity()
            self.screen.fill(black)
            self.screen.blit(self.ship, self.shiprect)
            pygame.draw.circle(self.screen, (255, 0, 0), (int(self.width/2), int(self.height/2)), 10, 0)
            pygame.display.flip()
            pygame.time.wait(33)
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
