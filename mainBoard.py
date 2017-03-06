""" Experiment with face detection and image filtering using OpenCV """
import shipClass

import os
import sys
import pygame
from pygame.locals import *
import random
import math

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


class BoardInit:
    def rotShip(self, myangle, shipNum):
        self.ships[shipNum].rotatecw(angle=myangle)
        self.shipImages[shipNum] = rot_center(self.shipImage, self.ships[shipNum].get_angle_from_vert())
        self.shiprects[shipNum] = self.shipImages[shipNum].get_rect()
        self.shiprects[shipNum] = self.shiprects[shipNum].move(self.ships[shipNum].pos[0], self.ships[shipNum].pos[1])

    def accelerate(self, shipNum):
        self.ships[shipNum].speed[0] -= (self.ships[shipNum].direct[0])
        self.ships[shipNum].speed[1] -= (self.ships[shipNum].direct[1])

    def moveShip(self, shipNum):
        myTime = self.detTime(shipNum)
        xc = self.ships[shipNum].speed[0]
        yc = self.ships[shipNum].speed[1]
        if shipNum == 0:
            myTime = 1
        self.shiprects[shipNum] = self.shiprects[shipNum].move(int(xc * myTime), int(yc * myTime))
        self.ships[shipNum].pos[0] += int(xc * myTime)
        self.ships[shipNum].pos[1] += int(yc * myTime)

    def gravity(self, shipNum):
        distance = self.distanceCent(shipNum)
        self.ships[shipNum].speed[0] -= ((self.ships[shipNum].pos[0]-self.center[0])/distance * .2)
        self.ships[shipNum].speed[1] -= ((self.ships[shipNum].pos[1]-self.center[1])/distance * .2)

    def distanceCent(self, shipNum):
        return ((self.ships[shipNum].pos[0]-self.center[0]) ** 2 + (self.ships[shipNum].pos[1] - self.center[1]) ** 2) ** .5

    def detTime(self, shipNum):
        distance = self.distanceCent(shipNum)
        print(distance)
        return distance / (distance + 500)

    def checkBounds(self, shipNum):
        if self.shiprects[shipNum].left < 0 or self.shiprects[shipNum].right > self.width:
            self.ships[shipNum].speed[0] = 0
        if self.shiprects[shipNum].top < 0 or self.shiprects[shipNum].bottom > self.height:
            self.ships[shipNum].speed[1] = 0
        if (abs(self.ships[shipNum].pos[1] - self.center[1]) < 50 or abs(self.ships[shipNum].pos[1] - self.center[1]) < 50) and (abs(self.ships[shipNum].pos[0] - self.center[0]) < 50 or
                                                                                                                                abs(self.ships[shipNum].pos[0] - self.center[0]) < 50):
            del self.ships[shipNum]
            del self.shiprects[shipNum]
            del self.shipImages[shipNum]

    def makeShip(self, tdirect = [0,1], tspeed = [0,0], tpos = [600,600]):
        self.ships.append(shipClass.Ship(direct=tdirect, speed =tspeed, pos = tpos))
        self.shipImages.append(self.shipImage.copy())
        shiprect = self.ship.get_rect()
        self.shiprects.append(shiprect.move(self.ships[len(self.ships)-1].pos))

    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 1800, 1000
        black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        # ball = pygame.draw.circle(self.screen, (255, 0, 0), (10, 10), 10, 0)
        self.center = [self.width/2, self.height/2]
        self.shipImage = pygame.image.load(os.path.join('rocket.png'))
        self.shipImage = pygame.transform.scale(self.shipImage, (50, 50))
        self.shipImage = pygame.transform.rotate(self.shipImage, -45)
        self.ship = self.shipImage.copy()
        self.shiprect = self.ship.get_rect()
        self.ships = []
        self.shipImages = []
        self.shiprects = []
        self.ships.append(shipClass.Ship(direct = [0,1], speed = [0,0], pos=[500,500]))
        self.shiprect = self.shiprect.move(self.ships[0].pos)
        self.shipImages.append(self.shipImage.copy())
        self.shiprects.append(self.shiprect)
        self.makeShip(tspeed=[2, 0])
        self.makeShip(tpos=[100, 100])
        self.makeShip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_LEFT]:
                self.rotShip(10, 0)
            if keys[pygame.K_RIGHT]:
                self.rotShip(-10, 0)
            if keys[pygame.K_SPACE]:
                self.accelerate(0)
            self.screen.fill(black)
            i = 0
            while i < len(self.ships):
                self.moveShip(i)
                self.gravity(i)
                self.rotShip(0, i)
                self.screen.blit(self.shipImages[i], self.shiprects[i])
                self.checkBounds(i)
                i += 1

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
