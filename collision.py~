import ogre.renderer.OGRE as ogre
import math
from vector import Vector3

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
                if ("Sleek" in self.ent.uiname or "Destroyer" in self.ent.uiname):
                    self.distance = self.ent.pos.squaredDistance(ent.pos)
                    if self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                        self.ent.vel.x = push * -1 * math.cos(math.radians(self.ent.heading))
                        self.ent.vel.z = push * -1 * math.sin(math.radians(self.ent.heading))
                        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
                        self.ent.desiredSpeed = 0
                        self.ent.speed = 0
                elif "Item_Weapon" in self.ent.uiname and (self.ent.pickedUp and self.ent.visible and (self.ent.held == False)):
                    self.distance = self.ent.pos.squaredDistance(ent.pos)
                    if ("Sleek" in ent.uiname or "Destroyer" in ent.uiname) and (self.ent.firedFrom != ent.uiname and self.ent.firedFrom != "0") and self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                        ent.hit = True
                        self.ent.visible = False
                        self.ent.aspects[1].node.setVisible(False)
                        self.ent.speed = 0
                        self.ent.desiredSpeed = 0
                        self.ent.desiredHeading = 0
                        self.ent.engine.entityMgr.weaponList.remove(self.ent)

        for ent in self.ent.engine.entityMgr.lvl1List:
            if not ent == self.ent:
                if not "Obstacle" in self.ent.uiname and not "Item_Boost" in self.ent.uiname:
                    self.distance = self.ent.pos.squaredDistance(ent.pos)
                    if "Item_Weapon" in self.ent.uiname:
                        if self.ent.pickedUp == True:
                            #we are a picked up missile
                            if self.ent.visible == True:
                                #we are a visible, picked up missile
                                if self.ent.held == True:
                                    #we are an unfired, held missile
                                    pass
                                else:
                                    #we are a fired, visible missile
                                    if "Obstacle" in ent.uiname and self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                                        self.ent.visible = False
                                        self.ent.aspects[1].node.setVisible(False)
                                        self.ent.speed = 0
                                        self.ent.desiredSpeed = 0
                                        self.ent.desiredHeading = 0
                                        self.ent.engine.entityMgr.weaponList.remove(self.ent)
                            else:
                                #we are an invisible, already done firing missile
                                pass
                        else:
                            #we have not been picked up yet
                            pass
                            
                    if "Sleek" in self.ent.uiname or "Destroyer" in self.ent.uiname:    
                        if self.distance <= self.collisionRange*self.collisionRange + ent.collisionRange*ent.collisionRange:
                            if "Item_Boost" in ent.uiname:
                                if ent.used == False:
                                    ent.aspects[1].pEnt.setVisible(False)
                                    self.ent.boosting = True
                                    ent.used = True
                            elif "Item_Weapon" in ent.uiname:
                                if ent.pickedUp == False and self.ent.weaponUp == False:
                                    #ent.aspects[1].pEnt.setVisible(False)
                                    self.ent.heldWeapon = ent
                                    self.ent.weaponUp = True
                                    ent.aspects[1].node.detachObject(ent.aspects[1].pEnt)
                                    ent.aspects[1].node = self.ent.aspects[1].node.createChildSceneNode()
                                    ent.aspects[1].node.position += Vector3(0,20,4)
                                    ent.aspects[1].node.scale(Vector3(10,10,10))
                                    ent.aspects[1].node.attachObject(ent.aspects[1].pEnt)
                                    ent.pickedUp = True
                                    ent.aspects[1].pEnt.setVisible(True)
                                    ent.visible = True
                            else:
                                self.ent.vel.x = push * -1 * math.cos(math.radians(self.ent.heading))
                                self.ent.vel.z = push * -1 * math.sin(math.radians(self.ent.heading))
                                self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
                                self.ent.desiredSpeed = 0
                                self.ent.speed = 0

        #if(self.ent.engine.entityMgr.entList[0].bulletList[0])
