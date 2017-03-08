class Bullet:

    def __init__(self, pos = [100, 100], dir = [1,0], speed = 10, bounceable = True):
        """not used"""
        self.pos = pos
        self.dir = dir
        self.speed = speed
        self.bounceable = bounceable

    def __str__(self):
        return "Nyoooom!"

    def get_velocity(self):
        return [self.dir[0] * self.speed, self.dir[1] * self.speed]

    def bounce(self):
        if self.bounceable == True:
            self.dir = [-self.dir[0], -self.dir[1]]

    def move(self):
        self.pos[0] += self.get_velocity()[0]
        self.pos[1] += self.get_velocity()[1]
