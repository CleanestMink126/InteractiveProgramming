import math

class Ship:

    def __init__(self, pos = None, direct = None, thrust = None, speed = None):
        """init for ships and other objects aswell"""
        if(pos is None):
            pos = [0,0]
        if(direct is None):
            direct = [1,0]
        if(thrust is None):
            thrust = 0
        if(speed is None):
            speed = [0,0]


        self.pos = pos
        self.direct = direct
        self.thrust = thrust
        self.speed = speed
        self.cargo = ["cat"]                #   Stowaway cat

    def __str__(self):
        return "Hello. I am a spaceship."   #   Because I can that's why

    def rotatecw(self, angle = 90):
        """rotates the direction o the ship by the given degrees
        note direction is in xy"""
        angle = deg2rad(angle)
        x = self.direct[0]
        y = self.direct[1]
        newx = math.cos(angle) * x + math.sin(angle) * y
        newy = - math.sin(angle) * x + math.cos(angle) * y
        self.direct = [newx, newy]

    def add_cargo(self, item):              #   This is necessary
        """idk why theres cargo"""
        self.cargo.append(item)

    def jettison(self, item):
        self.cargo.remove(item)

    def check_cargo(self):
        print("Items in cargo:")
        for item in self.cargo:
            print(item)

    def get_angle_from_vert(self):
        """returns the angle the ship is from verticle in order for the main class to get the correct angle image"""
        norm = math.sqrt(self.direct[0]**2 + self.direct[1]**2)
        x = self.direct[0]/norm
        y = self.direct[1]/norm
        if x >= 0 and y > 0:
            angle = math.asin(x)
        elif x > 0 and y <= 0:
            angle = math.pi/2 + math.asin(abs(y))
        elif x < 0 and y <= 0:
            angle = math.pi + math.asin(abs(x))
        else:
            angle = 3*math.pi/2 + math.asin(y)
        return rad2deg(angle)

def deg2rad(angle):
    return angle*math.pi/180

def rad2deg(angle):
    return angle*180/math.pi
