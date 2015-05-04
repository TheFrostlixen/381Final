#control manager, get input and update entity headings
#Andrew Menard and Brian Gaunt
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ent
from ent import *


class ControlMgr:
    def __init__(self, engine):
        self.engine = engine
        self.ent = ent

    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.stopped = False      

    def tick(self, dt):
        if self.stopped == True:
            return
            
        self.keyboard.capture()
        
        self.player1 = self.engine.entityMgr.entList[0]
        self.player2 = self.engine.entityMgr.entList[1]

        self.mainMenu = self.engine.inputMgr.inputListener.mainMenu
        

        if not self.mainMenu:
            if not self.keyboard.isKeyDown(OIS.KC_UP) and not self.player1.boosting:
                self.player1.slowDown = True

            if self.keyboard.isKeyDown(OIS.KC_UP):
                nextAccel = self.player1.speed + self.player1.acceleration
                if nextAccel < self.player1.maxSpeed:
                    self.player1.desiredSpeed += self.player1.acceleration
                    self.player1.slowDown = False
            
            if self.keyboard.isKeyDown(OIS.KC_DOWN):
                nextDecel = self.player1.speed - self.player1.acceleration
                if self.player1.desiredSpeed > 0:
                    self.player1.speed -= self.player1.acceleration
                if nextDecel > (-1*self.player1.maxSpeed/2):
                    self.player1.desiredSpeed -= self.player1.acceleration
                        
            if self.keyboard.isKeyDown(OIS.KC_LEFT) or self.engine.inputMgr.joysticks[0].get_axis(0) < -.6:
                if self.player1.desiredHeading < 0:
                    self.player1.desiredHeading = 360
                    self.player1.yaw = 360
                    self.player1.currentYaw = 360
                if self.player1.speed > 0 or self.player1.speed < -1:
                    self.player1.desiredHeading -= self.player1.turningRate
                    self.player1.yaw -= self.player1.turningRate
                        
            if self.keyboard.isKeyDown(OIS.KC_RIGHT) or self.engine.inputMgr.joysticks[0].get_axis(0) > .6:
                if self.player1.desiredHeading > 360:
                    self.player1.desiredHeading = 0
                    self.player1.yaw = 0
                    self.player1.currentYaw = 0
                if self.player1.speed > 0 or self.player1.speed < -1:
                    self.player1.desiredHeading += self.player1.turningRate
                    self.player1.yaw += self.player1.turningRate

            if self.keyboard.isKeyDown(OIS.KC_SLASH) and self.player1.loaded == True:
                self.player1.loaded = False
                bullet = self.ent.firstBullet(self.engine, 99, pos = self.player1.pos, heading = self.player1.heading, speed = 1)
                bullet.init()
                self.engine.entityMgr.lvl1List.append(bullet)
                self.player1.bulletList.append(bullet)
                print "pewpew1"

            if self.keyboard.isKeyDown(OIS.KC_ADD) and self.player2.loaded == True:
                print "pewpew2"

            if self.player1.slowDown == True:
                if self.player1.desiredSpeed > 0:
                    self.player1.desiredSpeed -= (self.player1.acceleration / 2)


        if not self.mainMenu:
            if not self.keyboard.isKeyDown(OIS.KC_NUMPAD8):# or self.engine.inputMgr.jMgr.triggerRDown:
                self.player2.slowDown = True

            if self.keyboard.isKeyDown(OIS.KC_NUMPAD8):# or self.engine.inputMgr.jMgr.triggerRDown:
                nextAccel = self.player2.speed + self.player2.acceleration
                if nextAccel < self.player2.maxSpeed:
                    self.player2.desiredSpeed += self.player2.acceleration
                    self.player2.slowDown = False
            
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD5):# or self.engine.inputMgr.jMgr.triggerLDown:
                nextDecel = self.player2.speed - self.player2.acceleration
                if nextDecel > (-1*self.player2.maxSpeed/2):
                    self.player2.desiredSpeed -= self.player2.acceleration
                        
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD4):# or self.engine.inputMgr.jMgr.joyLDown:
                if self.player2.desiredHeading < 0:
                    self.player2.desiredHeading = 360
                    self.player2.yaw = 360
                    self.player2.currentYaw = 360
                if self.player2.speed > 0 or self.player2.speed < -1:
                    self.player2.desiredHeading -= self.player2.turningRate
                    self.player2.yaw -= self.player2.turningRate
                    
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD6):# or self.engine.inputMgr.jMgr.joyRDown:
                if self.player2.desiredHeading > 360:
                    self.player2.desiredHeading = 0
                    self.player2.yaw = 0
                    self.player2.currentYaw = 0
                if self.player2.speed > 0 or self.player2.speed < -1:
                    self.player2.desiredHeading += self.player2.turningRate
                    self.player2.yaw += self.player2.turningRate

            if self.player2.slowDown == True:
                if self.player2.desiredSpeed > 0:
                    self.player2.desiredSpeed -= (self.player2.acceleration / 2)


        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            for ent in self.engine.entityMgr.entList:
                ent.speed = 0
                ent.desiredSpeed = 0
        

    def stop(self):
        self.stopped = True
        

    















