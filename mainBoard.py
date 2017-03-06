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

    def rotRock(self, myangle, shipNum):
        self.ships[shipNum].rotatecw(angle=myangle)
        self.shipImages[shipNum] = rot_center(self.rockImage, self.ships[shipNum].get_angle_from_vert())
        self.shiprects[shipNum] = self.shipImages[shipNum].get_rect()
        self.shiprects[shipNum] = self.shiprects[shipNum].move(self.ships[shipNum].pos[0], self.ships[shipNum].pos[1])


    def accelerate(self, shipNum):
        self.ships[shipNum].speed[0] -= (self.ships[shipNum].direct[0])
        self.ships[shipNum].speed[1] -= (self.ships[shipNum].direct[1])

    def moveShip(self, shipNum):
        myTime = self.detTime(shipNum)
        mainTime = self.detTime(0)
        xc = self.ships[shipNum].speed[0]
        yc = self.ships[shipNum].speed[1]
        if shipNum == 0:
            myTime = 1
            mainTime = 1
        self.ships[shipNum].pos[0] += ((xc * myTime)/mainTime)
        self.ships[shipNum].pos[1] += ((yc * myTime)/mainTime)


    def gravity(self, shipNum):
        distance = self.distanceCent(shipNum)
        myTime = self.detTime(shipNum)
        mainTime = self.detTime(0)
        if shipNum == 0:
            myTime = 1
            mainTime = 1
        self.ships[shipNum].speed[0] -= myTime * ((self.ships[shipNum].pos[0]-self.center[0])/distance * .6)/mainTime
        self.ships[shipNum].speed[1] -= myTime * ((self.ships[shipNum].pos[1]-self.center[1])/distance * .6)/mainTime
        if mainTime < 0:
            print("fuckin weird shit")
        if myTime < 0:
            print("more weird shit")
        if distance < 0:
            print("no, that's weird")


    def distanceCent(self, shipNum):
        return ((self.ships[shipNum].pos[0]-self.center[0]) ** 2 + (self.ships[shipNum].pos[1] - self.center[1]) ** 2) ** .5


    def detTime(self, shipNum):
        distance = self.distanceCent(shipNum)
        # print(distance)
        return distance / (distance + 500)

    def checkBounds(self, shipNum):
        if(shipNum > 0):
            print("NO THIS DOES NOT HAPPEN")
        if self.shiprects[shipNum].left < 0:
            self.ships[shipNum].speed[0] = 5
        if self.shiprects[shipNum].right > self.width:
            self.ships[shipNum].speed[0] = -5
        if self.shiprects[shipNum].top < 0:
            self.ships[shipNum].speed[1] = 5
        if self.shiprects[shipNum].bottom > self.height:
            self.ships[shipNum].speed[1] = -5
    def checkHole(self, shipNum):
        if (abs(self.ships[shipNum].pos[1] - self.center[1]) < 50 or abs(self.ships[shipNum].pos[1] - self.center[1]) < 50) and (abs(self.ships[shipNum].pos[0] - self.center[0]) < 50 or
                                                                                                                                abs(self.ships[shipNum].pos[0] - self.center[0]) < 50):
            del self.ships[shipNum]
            del self.shiprects[shipNum]
            del self.shipImages[shipNum]

    def makeShip(self, tdirect = None, tspeed = None, tpos = None):

        if(tpos is None):
            tpos = [600,600]
        if(tdirect is None):
            direct = [0,1]
        if(tspeed is None):
            tspeed = [0,0]

        self.ships.append(shipClass.Ship(direct=tdirect, speed =tspeed, pos = tpos))
        self.shipImages.append(self.rockImage.copy())
        newrect = self.ship.get_rect()
        self.shiprects.append(newrect.move(self.ships[len(self.ships)-1].pos))

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
        self.rockImage = pygame.image.load(os.path.join('rock.png'))
        self.rockImage = pygame.transform.scale(self.rockImage, (50, 50))
        self.ship = self.shipImage.copy()
        self.shiprect = self.ship.get_rect()
        self.ships = []
        self.shipImages = []
        self.shiprects = []
        self.ships.append(shipClass.Ship(direct = [0,1], speed = [0,0], pos=[100,100]))
        self.shiprect = self.shiprect.move(self.ships[0].pos)
        self.shipImages.append(self.shipImage.copy())
        self.shiprects.append(self.shiprect)
        self.makeShip(tpos=[1000, 1000],tspeed=[10, 0])
        self.makeShip(tpos=[500, 500],tspeed=[0, 10])
        self.makeShip(tpos=[100, 100],tspeed=[10, 0])
        self.makeShip(tspeed=[50, 0])
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
            self.rotShip(0, i)
            while i < len(self.ships):
                if i > 0:
                    self.rotRock(10, i)
                else:
                    self.checkBounds(i)
                self.moveShip(i)
                self.gravity(i)
                self.screen.blit(self.shipImages[i], self.shiprects[i])
                #self.checkHole(i)
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
