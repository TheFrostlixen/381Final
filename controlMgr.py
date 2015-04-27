#control manager, get input and update entity headings
#Andrew Menard and Brian Gaunt
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS


class ControlMgr:
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.stopped = False
        self.camera1 = self.engine.inputMgr.inputListener.camNode_P1

    def tick(self, dt):
        if self.stopped == True:
            return
            
        self.keyboard.capture()
        
        self.player1 = self.engine.entityMgr.entList[0]
        self.player2 = self.engine.entityMgr.entList[1]


        if not self.engine.inputMgr.inputListener.intro:
            if self.keyboard.isKeyDown(OIS.KC_UP):
                nextAccel = self.player1.speed + self.player1.acceleration
                if nextAccel < self.player1.maxSpeed:
                    self.player1.desiredSpeed += self.player1.acceleration
            
            if self.keyboard.isKeyDown(OIS.KC_DOWN):
                nextDecel = self.player1.speed - self.player1.acceleration
                if nextDecel > (-1*self.player1.maxSpeed/2):
                    self.player1.desiredSpeed -= self.player1.acceleration
                        
            if self.keyboard.isKeyDown(OIS.KC_LEFT):
                if self.player1.desiredHeading < 0:
                    self.player1.desiredHeading = 360
                    self.player1.yaw = 360
                    self.player1.currentYaw = 360
                if self.player1.speed > 0 or self.player1.speed < -1:
                    self.player1.desiredHeading -= self.player1.turningRate
                    self.player1.yaw -= self.player1.turningRate
                    
            if self.keyboard.isKeyDown(OIS.KC_RIGHT):
                if self.player1.desiredHeading > 360:
                    self.player1.desiredHeading = 0
                    self.player1.yaw = 0
                    self.player1.currentYaw = 0
                if self.player1.speed > 0 or self.player1.speed < -1:
                    self.player1.desiredHeading += self.player1.turningRate
                    self.player1.yaw += self.player1.turningRate

        if not self.engine.inputMgr.inputListener.intro:
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD8) or self.engine.inputMgr.jMgr.triggerRDown:
                nextAccel = self.player2.speed + self.player2.acceleration
                if nextAccel < self.player2.maxSpeed:
                    self.player2.desiredSpeed += self.player2.acceleration
            
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD5) or self.engine.inputMgr.jMgr.triggerLDown:
                nextDecel = self.player2.speed - self.player2.acceleration
                if nextDecel > (-1*self.player2.maxSpeed/2):
                    self.player2.desiredSpeed -= self.player2.acceleration
                        
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD4) or self.engine.inputMgr.jMgr.joyLDown:
                if self.player2.desiredHeading < 0:
                    self.player2.desiredHeading = 360
                    self.player2.yaw = 360
                    self.player2.currentYaw = 360
                if self.player2.speed > 0 or self.player2.speed < -1:
                    self.player2.desiredHeading -= self.player2.turningRate
                    self.player2.yaw -= self.player2.turningRate
                    
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD6) or self.engine.inputMgr.jMgr.joyRDown:
                if self.player2.desiredHeading > 360:
                    self.player2.desiredHeading = 0
                    self.player2.yaw = 0
                    self.player2.currentYaw = 0
                if self.player2.speed > 0 or self.player2.speed < -1:
                    self.player2.desiredHeading += self.player2.turningRate
                    self.player2.yaw += self.player2.turningRate


        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            for ent in self.engine.entityMgr.entList:
                ent.speed = 0
                ent.desiredSpeed = 0
        

    def stop(self):
        self.stopped = True
        

    















