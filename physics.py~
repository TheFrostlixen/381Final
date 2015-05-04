#Andrew Menard and Brian Gaunt
import math

class Physics:
    def __init__(self, ent):
        self.ent = ent
        self.boosted = False
        self.boostTime = 0
        
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


        if self.ent.heading >= 360:
            self.ent.heading = 0
        if self.ent.heading < 0:
            self.ent.heading = 357
        
        if self.ent.desiredHeading >= 360:
            self.ent.desiredHeading = 0
        if self.ent.desiredHeading < 0:
            self.ent.desiredHeading = 357

        if self.ent.boosting and not self.boosted:
            self.ent.slowDown = False
            self.ent.acceleration *= 100
            self.ent.maxSpeed *= 2
            self.ent.turningRate *= 2
            self.boosted = True
        if self.boostTime < 0.5 and self.boosted:
            self.boostTime += dtime
        elif self.boosted == True:
            self.ent.acceleration /= 100
            self.ent.maxSpeed /= 2
            self.ent.turningRate /= 2
            self.boosted = False
            self.boostTime = 0
            self.ent.boosting = False
            
        self.ent.vel.x = self.ent.speed * math.cos(math.radians(self.ent.heading))
        self.ent.vel.z = self.ent.speed * math.sin(math.radians(self.ent.heading))
        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)


