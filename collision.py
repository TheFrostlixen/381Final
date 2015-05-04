import ogre.renderer.OGRE as ogre
import math

class Collision:
    def __init__(self, ent):
        self.ent = ent
        self.id = self.ent.eid
        self.collisionRange = ent.collisionRange
        
    def tick(self, dtime):
        
        push = self.ent.maxSpeed
        if self.ent.speed < 0:
            push = self.ent.maxSpeed*-1

        for ent in self.ent.engine.entityMgr.entList:
            if not ent == self.ent:
                self.distance = self.ent.pos.squaredDistance(ent.pos)
                if self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                    self.ent.vel.x = push * -1 * math.cos(math.radians(self.ent.heading))
                    self.ent.vel.z = push * -1 * math.sin(math.radians(self.ent.heading))
                    self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
                    self.ent.desiredSpeed = 0
                    self.ent.speed = 0


        for ent in self.ent.engine.entityMgr.lvl1List:
            if not ent == self.ent:
                    self.distance = self.ent.pos.squaredDistance(ent.pos)
                    if self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                        if "Item_Boost" in ent.uiname:
                            if ent.used == False:
                                ent.aspects[1].pEnt.setVisible(False)
                                self.ent.boosting = True
                                ent.used = True
                        elif "Item_Weapon" in ent.uiname:
                            if ent.used == False:
                                ent.aspects[1].pEnt.setVisible(False)
                                self.ent.weaponUp = True
                                self.ent.loaded = True
                        elif "bullet" in ent.uiname:
                            pass
                        else:
                            self.ent.vel.x = push * -1 * math.cos(math.radians(self.ent.heading))
                            self.ent.vel.z = push * -1 * math.sin(math.radians(self.ent.heading))
                            self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
                            self.ent.desiredSpeed = 0
                            self.ent.speed = 0

        #if(self.ent.engine.entityMgr.entList[0].bulletList[0])
