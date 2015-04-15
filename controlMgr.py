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
        if self.keyboard.isKeyDown(OIS.KC_UP):
            for ent in self.engine.selectionMgr.selectedEnts:
                nextAccel = ent.speed + ent.acceleration
                if nextAccel < ent.maxSpeed:
                    ent.desiredSpeed += ent.acceleration
        
        if self.keyboard.isKeyDown(OIS.KC_DOWN):
            for ent in self.engine.selectionMgr.selectedEnts:
                nextDecel = ent.speed - ent.acceleration
                if nextDecel > (-1*ent.maxSpeed/2):
                    ent.desiredSpeed -= ent.acceleration
                    
        if self.keyboard.isKeyDown(OIS.KC_LEFT):
            for ent in self.engine.selectionMgr.selectedEnts:
                if ent.desiredHeading < 0:
                    ent.desiredHeading = 360
                    ent.yaw = 360
                    ent.currentYaw = 360
                if ent.speed > 0 or ent.speed < -1:
                    ent.desiredHeading -= ent.turningRate
                    ent.yaw -= ent.turningRate
                
        if self.keyboard.isKeyDown(OIS.KC_RIGHT):
            for ent in self.engine.selectionMgr.selectedEnts:
                if ent.desiredHeading > 360:
                    ent.desiredHeading = 0
                    ent.yaw = 0
                    ent.currentYaw = 0
                if ent.speed > 0 or ent.speed < -1:
                    ent.desiredHeading += ent.turningRate
                    ent.yaw += ent.turningRate
        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            for ent in self.engine.selectionMgr.selectedEnts:
                ent.speed = 0
                ent.desiredSpeed = 0
        

    def stop(self):
        self.stopped = True
        

    















