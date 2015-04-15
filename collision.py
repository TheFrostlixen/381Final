import ogre.renderer.OGRE as ogre
import math

class Collision:
    def __init__(self, ent):
        self.ent = ent
        self.id = self.ent.eid
        self.collisionRange = ent.collisionRange
        
    def tick(self, dtime):
        
        for ent in self.ent.engine.entityMgr.entList:
            if not ent == self.ent:
                self.distance = self.ent.pos.squaredDistance(ent.pos)
                if self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                    self.ent.vel.x = self.ent.maxSpeed * -1 * math.cos(math.radians(self.ent.heading))
                    self.ent.vel.z = self.ent.maxSpeed * -1 * math.sin(math.radians(self.ent.heading))
                    self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
                    self.ent.desiredSpeed = 0
                    self.ent.speed = 0


        for ent in self.ent.engine.entityMgr.lvl1List:
            if not ent == self.ent:
                self.distance = self.ent.pos.squaredDistance(ent.pos)
                if self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                    self.ent.vel.x = self.ent.maxSpeed * -1 * math.cos(math.radians(self.ent.heading))
                    self.ent.vel.z = self.ent.maxSpeed * -1 * math.sin(math.radians(self.ent.heading))
                    self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
                    self.ent.desiredSpeed = 0
                    self.ent.speed = 0
