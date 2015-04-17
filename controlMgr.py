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

    def tick(self, dt):
        if self.stopped == True:
            return
            
        self.keyboard.capture()
        
        player1 = self.engine.entityMgr.entList[0]
        player2 = self.engine.entityMgr.entList[1]
        
        if self.keyboard.isKeyDown(OIS.KC_UP):
            nextAccel = player1.speed + player1.acceleration
            if nextAccel < player1.maxSpeed:
                player1.desiredSpeed += player1.acceleration
        
        if self.keyboard.isKeyDown(OIS.KC_DOWN):
            nextDecel = player1.speed - player1.acceleration
            if nextDecel > (-1*player1.maxSpeed/2):
                player1.desiredSpeed -= player1.acceleration
                    
        if self.keyboard.isKeyDown(OIS.KC_LEFT):
            if player1.desiredHeading < 0:
                player1.desiredHeading = 360
                player1.yaw = 360
                player1.currentYaw = 360
            if player1.speed > 0 or player1.speed < -1:
                player1.desiredHeading -= player1.turningRate
                player1.yaw -= player1.turningRate
                
        if self.keyboard.isKeyDown(OIS.KC_RIGHT):
            if player1.desiredHeading > 360:
                player1.desiredHeading = 0
                player1.yaw = 0
                player1.currentYaw = 0
            if player1.speed > 0 or player1.speed < -1:
                player1.desiredHeading += player1.turningRate
                player1.yaw += player1.turningRate

        if self.keyboard.isKeyDown(OIS.KC_NUMPAD8):
            nextAccel = player2.speed + player2.acceleration
            if nextAccel < player2.maxSpeed:
                player2.desiredSpeed += player2.acceleration
        
        if self.keyboard.isKeyDown(OIS.KC_NUMPAD5):
            nextDecel = player2.speed - player2.acceleration
            if nextDecel > (-1*player2.maxSpeed/2):
                player2.desiredSpeed -= player2.acceleration
                    
        if self.keyboard.isKeyDown(OIS.KC_NUMPAD4):
            if player2.desiredHeading < 0:
                player2.desiredHeading = 360
                player2.yaw = 360
                player2.currentYaw = 360
            if player2.speed > 0 or player2.speed < -1:
                player2.desiredHeading -= player2.turningRate
                player2.yaw -= player2.turningRate
                
        if self.keyboard.isKeyDown(OIS.KC_NUMPAD6):
            if player2.desiredHeading > 360:
                player2.desiredHeading = 0
                player2.yaw = 0
                player2.currentYaw = 0
            if player2.speed > 0 or player2.speed < -1:
                player2.desiredHeading += player2.turningRate
                player2.yaw += player2.turningRate


        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            for ent in self.engine.entityMgr.entList:
                ent.speed = 0
                ent.desiredSpeed = 0
        

    def stop(self):
        self.stopped = True
        

    















