import math

class Ship:

    def __init__(self, pos = [100, 100], direct = [1, 0], thrust = 0, speed = 0):
        self.pos = pos
        self.direct = direct
        self.thrust = thrust
        self.speed = speed
        self.cargo = ["cat"]                #   Stowaway cat

    def __str__(self):
        return "Hello. I am a spaceship."   #   Because I can that's why

    def rotatecw(self, angle = 90):
        angle = deg2rad(angle)
        x = self.direct[0]
        y = self.direct[1]
        newx = math.cos(angle) * x + math.sin(angle) * y
        newy = - math.sin(angle) * x + math.cos(angle) * y
        self.direct = [newx, newy]

    def add_cargo(self, item):              #   This is necessary
        self.cargo.append(item)

    def jettison(self, item):
        self.cargo.remove(item)

    def check_cargo(self):
        print("Items in cargo:")
        for item in self.cargo:
            print(item)

def deg2rad(angle):
    return angle*math.pi/180
