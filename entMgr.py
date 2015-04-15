#Entity Manager
#Andrew Menard and Brian Gaunt
import ogre.renderer.OGRE as ogre

class EntityManager:
    def __init__(self, engine):
        print "starting entity manager"
        self.engine = engine
        
    def init(self):
        self.entList = []
        self.numEnts = 0
        
        import ent
        self.entTypes = [ent.Carrier, ent.Sleek, ent.SailBoat, ent.Missile, ent.CigaretteBoat,
                         ent.Boat, ent.JetSki, ent.Yacht, ent.SpeedBoat, ent.Destroyer]
        
    def createEnt(self, entType, pos = ogre.Vector3(0,0,0)):
        ent = entType(self.engine, self.numEnts, pos = pos)
        ent.init()
        self.entList[numEnts] = ent
        self.numEnts = self.numEnts + 1
        return ent

    def tick(self, dt):
        for ent in self.entList:
            ent.tick(dt)
        
    def stop(self):
        pass

        #mine
        
    
