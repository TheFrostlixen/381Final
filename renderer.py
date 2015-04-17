#Andrew Menard and Brian Gaunt
import ogre.renderer.OGRE as ogre
import math

class Renderer():

    def __init__(self, ent):
        self.ent = ent
        
        self.pEnt = self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + str(self.ent.eid), self.ent.mesh)
        self.node = self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'node' + str(self.ent.pos), ent.pos)
        self.node.attachObject(self.pEnt)
        self.pEnt.setMaterialName('Material #8')
        
        if self.ent.uiname != "Obstacle":
            self.wakenode = self.node.createChildSceneNode()
            self.wakeparticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + "Wake_entity", 'Examples/Wake')
            self.wakenode.attachObject(self.wakeparticle)
            self.wakenode.setPosition(ogre.Vector3(-60,-8,0))

        if(self.ent.mesh == "missile.mesh"):
            self.node.scale(ogre.Vector3(4,4,4))
        
        
    def tick(self, dt):
        #if(self.node != 0):

            self.node.position = self.ent.pos
            
            if self.ent.currentYaw < self.ent.yaw:
                self.node.yaw(-1*math.radians(self.ent.turningRate))
                self.ent.currentYaw += self.ent.turningRate
                
            if self.ent.currentYaw > self.ent.yaw:
                self.node.yaw(math.radians(self.ent.turningRate))
                self.ent.currentYaw -= self.ent.turningRate
                
            self.node.showBoundingBox(self.ent.isSelected)
