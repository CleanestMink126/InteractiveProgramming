import shipClass
import score_class

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
        """rotate the main ship"""
        self.ships[shipNum].rotatecw(angle=myangle)
        """changes the ship object in the list of ships"""
        self.shipImages[shipNum] = rot_center(self.shipImage, self.ships[shipNum].get_angle_from_vert())
        """this will call the function to rotate the ship image about its center"""
        self.shiprects[shipNum] = self.shipImages[shipNum].get_rect()
        """this will grab the bounding box of the new ship"""
        self.shiprects[shipNum] = self.shiprects[shipNum].move(self.ships[shipNum].pos[0], self.ships[shipNum].pos[1])
        """this will move the box to the position of the ship"""

    def rotRock(self, myangle, shipNum):
        myangle /= self.detTime(0)
        """this will change the angle of rotation based on the distance of the player ship from the blackhole"""
        """the rest is the same as rot ship"""
        self.ships[shipNum].rotatecw(angle=myangle)
        self.shipImages[shipNum] = rot_center(self.rockImage, self.ships[shipNum].get_angle_from_vert())
        self.shiprects[shipNum] = self.shipImages[shipNum].get_rect()
        self.shiprects[shipNum] = self.shiprects[shipNum].move(self.ships[shipNum].pos[0], self.ships[shipNum].pos[1])


    def accelerate(self, shipNum):
        """will add current direction of ship to speed to simulate thrust"""
        self.ships[shipNum].speed[0] -= (self.ships[shipNum].direct[0])
        self.ships[shipNum].speed[1] -= (self.ships[shipNum].direct[1])

    def moveShip(self, shipNum):
        """this will move all objects forward according to their speed"""
        """the time is determined for non-player ship object to simulate time dialation"""
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
        """this simulated the effect of gravity, also adjusted for time dialation"""
        distance = self.distanceCent(shipNum)
        myTime = self.detTime(shipNum)
        mainTime = self.detTime(0)
        if shipNum == 0:
            myTime = 1
            mainTime = 1
        self.ships[shipNum].speed[0] -= myTime * ((self.ships[shipNum].pos[0]-self.center[0])/(distance ** 2) * 200)/mainTime
        self.ships[shipNum].speed[1] -= myTime * ((self.ships[shipNum].pos[1]-self.center[1])/(distance ** 2) * 200)/mainTime

    def distanceCent(self, shipNum):
        """returns distance from any object to black hole"""
        return ((self.ships[shipNum].pos[0]-self.center[0]) ** 2 + (self.ships[shipNum].pos[1] - self.center[1]) ** 2) ** .5


    def detTime(self, shipNum):
        """this will determine the time dialation based on distance from black hole"""
        distance = self.distanceCent(shipNum)
        # print(distance)
        return distance / (distance + 750)

    def checkBounds(self, shipNum):
        """this will make sure the player ship is within the screen, if not it will set its speeed to move it in screen"""
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
        """this will check to see if the given object is within the black hole, if it is, it deletes the object"""
        if (abs(self.ships[shipNum].pos[1] - self.center[1]) < 50 or abs(self.ships[shipNum].pos[1] - self.center[1]) < 50) and (abs(self.ships[shipNum].pos[0] - self.center[0]) < 50 or
                                                                                                                                abs(self.ships[shipNum].pos[0] - self.center[0]) < 50):
            del self.ships[shipNum]
            del self.shiprects[shipNum]
            del self.shipImages[shipNum]
            if(shipNum == 0):
                self.score_obj.dead = True
    def makeShip(self, tdirect = None, tspeed = None, tpos = None):
        """this will create an object (not necessarily a ship) with the given components"""
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

    def makeImages(self):
        """this will add all the of required images to variables so they are accessable
        and will adjust them to the correct size"""
        self.shipImage = pygame.image.load(os.path.join('rocket.png'))
        self.shipImage = pygame.transform.scale(self.shipImage, (50, 50))
        self.shipImage = pygame.transform.rotate(self.shipImage, -45)
        self.rockImage = pygame.image.load(os.path.join('rock.png'))
        self.rockImage = pygame.transform.scale(self.rockImage, (50, 50))
        self.holeImageOG = pygame.image.load(os.path.join('BlackHole.png'))
        self.holeImageOG = pygame.transform.scale(self.holeImageOG, (100, 100))
        self.glowyImage = pygame.image.load(os.path.join('glowy.png'))
        self.glowyImage = pygame.transform.scale(self.glowyImage, (50, 50))
        self.holerect = self.holeImageOG.get_rect()
        self.holerect = self.holerect.move(int(self.center[0]), int(self.center[1]))
        self.holeangle = 0

    def rotHole(self):
        """this will rotate the black hole cause why not """
        self.holeangle += .1/ self.detTime(0)
        if self.holeangle > 360:
            self.holeangle -= 360
        self.holeImage = rot_center(self.holeImageOG, self.holeangle)
        self.holerect = self.holeImage.get_rect()
        self.holerect = self.holerect.move(int(self.center[0]), int(self.center[1]))

    def shipCollide(self):
        """this will check if the ships bounding box intersects with any others,
        if it does, it will destroy the ship. The commented out code will cause the
        ship to bounce off instead"""
        if(self.shiprects[0].collidelist(self.shiprects[1:len(self.shiprects)]) != -1):
            del self.ships[0]
            del self.shiprects[0]
            del self.shipImages[0]
            self.score_obj.dead = True
        # collideIndex = self.shiprects[0].collidelist(self.shiprects[1:len(self.shiprects)])
        # if(collideIndex != -1):
        #     collideIndex += 1
        #     rock1 = self.ships[0]
        #     rock2 = self.ships[collideIndex]
        #     mag1 = ((rock1.speed[0] ** 2) + (rock1.speed[1] ** 2)) ** .5
        #     mag2 = ((rock2.speed[0] ** 2) + (rock2.speed[1] ** 2)) ** .5
        #     magAvg = (mag1 + mag2)/2
        #     rock1.speed[0], rock1.speed[1], rock2.speed[0], rock2.speed[1] = magAvg * rock2.speed[0]/mag2, magAvg * rock2.speed[1]/mag2, magAvg * rock1.speed[0]/mag1, magAvg * rock1.speed[1]/mag1
        #     self.moveShip(0)
        #     self.moveShip(collideIndex)
        #     self.moveShip(0)
        #     self.moveShip(collideIndex)

    def make_dot(self):
        """creates the dots that you have to collect in a random place"""
        self.dotrect = self.glowyImage.get_rect()
        self.dotrect = self.dotrect.move(random.randint(100, 1700), random.randint(100, 900))

    def check_dot(self):
        """this checks if the main ship's box is over the dot box
        if so, it makes and new dot, a new astroid, and increments the score"""
        if(self.dotrect.colliderect(self.shiprects[0]) or self.dotrect.colliderect(self.holerect)):
            self.make_dot()
            pos = [random.randint(100, 1700), random.randint(100, 900)]
            speed = [random.randint(-15, 15), random.randint(-15, 15)]
            self.makeShip(tpos=pos,tspeed=speed)
            if(not self.score_obj.dead):
                self.score_obj.score(1)


    def rockCollide(self):
        """checks if any of the rocks collide with one another,
        if so, it averages the speed and swtches the directions of both
        yes we know this isnt how physics works"""
        for i in range(1, len(self.shiprects)):
            collideIndex = self.shiprects[i].collidelist(self.shiprects[i+1:len(self.shiprects)])
            if(collideIndex != -1):
                collideIndex += 1 + i
                rock1 = self.ships[i]
                rock2 = self.ships[collideIndex]
                mag1 = ((rock1.speed[0] ** 2) + (rock1.speed[1] ** 2)) ** .5
                mag2 = ((rock2.speed[0] ** 2) + (rock2.speed[1] ** 2)) ** .5
                magAvg = (mag1 + mag2)/2
                rock1.speed[0], rock1.speed[1], rock2.speed[0], rock2.speed[1] = magAvg * rock2.speed[0]/mag2, magAvg * rock2.speed[1]/mag2, magAvg * rock1.speed[0]/mag1, magAvg * rock1.speed[1]/mag1

                self.moveShip(i)
                self.moveShip(collideIndex)
                self.moveShip(i)
                self.moveShip(collideIndex)
                # rock1.speed[0] = magAvg * rock2.speed[0]/mag2
                #rock1.speed[1] = magAvg * rock2.speed[1]/mag2
                #rock2.speed[0] = magAvg * rock1.speed[0]/mag1
                #rock2.speed[1] = magAvg * rock1.speed[1]/mag1

    def __init__(self):
        """this is where the game is set up and run"""
        pygame.init()
        """screen size"""
        self.size = self.width, self.height = 1800, 1000
        black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        # ball = pygame.draw.circle(self.screen, (255, 0, 0), (10, 10), 10, 0)
        self.center = [self.width/2, self.height/2]
        """this creates a score object to increment a score and tell if the player died"""
        self.score_obj = score_class.Score(self.screen, 50)
        self.makeImages()
        """below creates the main ship object and add it to the lists that keep track of the different asteroids"""
        self.ship = self.shipImage.copy()
        self.shiprect = self.ship.get_rect()
        self.ships = []
        self.shipImages = []
        self.shiprects = []
        self.ships.append(shipClass.Ship(direct = [0,1], speed = [0,0], pos=[100,100]))
        self.shiprect = self.shiprect.move(self.ships[0].pos)
        self.shipImages.append(self.shipImage.copy())
        self.shiprects.append(self.shiprect)
        # self.makeShip(tpos=[1000, 1000],tspeed=[10, 0])
        # self.makeShip(tpos=[500, 500],tspeed=[0, 10])
        # self.makeShip(tpos=[300, 100],tspeed=[10, 0])
        # self.makeShip(tspeed=[50, 0])
        self.make_dot()
        """this is the main loop for the game"""
        while 1:
            """detection of escape key to close program"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            """this detects the arrow keys for turning and space for accelerations"""
            keys = pygame.key.get_pressed()  #checking pressed keys
            if keys[pygame.K_LEFT]:
                self.rotShip(10, 0)
            if keys[pygame.K_RIGHT]:
                self.rotShip(-10, 0)
            if keys[pygame.K_SPACE]:
                self.accelerate(0)
            if keys[pygame.K_r]:
                board = BoardInit()

            self.screen.fill(black)
            i = 0
            """below rotates ship to uppdate position"""
            self.rotShip(0, i)
            """this loops over each ship and does the necessry operations on each"""
            while i < len(self.ships):
                if i > 0:
                    self.rotRock(2, i)
                else:
                    self.checkBounds(i)
                self.moveShip(i)
                self.gravity(i)
                """blit will tie the bounding box and image to the screen"""
                self.screen.blit(self.shipImages[i], self.shiprects[i])
                self.check_dot()
                self.checkHole(i)
                i += 1

            # pygame.draw.circle(self.screen, (255, 0, 0), (int(self.width/2), int(self.height/2)), 10, 0)
            self.rotHole()
            self.shipCollide()
            self.rockCollide()
            self.score_obj.render()
            self.screen.blit(self.holeImage, self.holerect)
            self.screen.blit(self.glowyImage, self.dotrect)
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
