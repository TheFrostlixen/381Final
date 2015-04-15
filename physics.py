#Andrew Menard and Brian Gaunt
import math

class Physics:
    def __init__(self, ent):
        self.ent = ent
        
    def tick(self, dtime):
        #print "Physics tick", dtime
        nextDecel = self.ent.speed - self.ent.acceleration
        nextAccel = self.ent.speed + self.ent.acceleration
        if self.ent.speed < self.ent.desiredSpeed - 1 and nextAccel < self.ent.maxSpeed:
            self.ent.speed += self.ent.acceleration
        if self.ent.speed > self.ent.desiredSpeed + 1 and nextDecel > -1*(self.ent.maxSpeed / 2):
            self.ent.speed -= self.ent.acceleration

        if self.ent.desiredHeading > self.ent.heading:
            if (self.ent.desiredHeading - self.ent.heading) > ((360 - self.ent.desiredHeading) + self.ent.heading):
                self.ent.heading -= self.ent.turningRate
            else:
                self.ent.heading += self.ent.turningRate
        elif self.ent.desiredHeading < self.ent.heading:
            if(self.ent.heading - self.ent.desiredHeading) > ((360 - self.ent.desiredHeading) + self.ent.heading):
                self.ent.heading += self.ent.turningRate
            else:
                self.ent.heading -= self.ent.turningRate
        if self.ent.heading > 360:
            self.ent.heading = 0
        if self.ent.heading < 0:
            self.ent.heading = 360

            
        self.ent.vel.x = self.ent.speed * math.cos(math.radians(self.ent.heading))
        self.ent.vel.z = self.ent.speed * math.sin(math.radians(self.ent.heading))
        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)

