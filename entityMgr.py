#Entity Manager        
from vector import Vector3    
import ent     
        
class EntityMgr:        
    def __init__(self, engine):        
        print "starting entity manager"        
        self.engine = engine        
                
    def init(self):        
        self.entList = []    
        self.lvl1List = []
        self.lvl1ChkPts = []
        self.numEnts = 0
        self.numObs = 0        

        self.entTypes = [ent.Sleek, ent.Destroyer]        

    def createEnt(self, entType, pos = Vector3(0,0,0)):        
        ent = entType(self.engine, self.numEnts, pos = pos)        
        ent.init()        
        self.entList.append(ent)        
        self.numEnts = self.numEnts + 1        
        return ent
                
    def createObs(self, pos = Vector3(0,0,0)):        
        obs = ent.Obstacle(self.engine, self.numObs, pos = pos)        
        obs.init()
        obs.uiname += str(self.numObs)
        print "flag"
        print obs.uiname
        self.lvl1List.append(obs)        
        self.numObs = self.numObs + 1        
        return obs
        
    def createLvl1(self):
        #create chkpt list
        for i in xrange(0,100):
            vector = Vector3(i * 100,0,0)
            self.lvl1ChkPts.append(vector)
            
        #create obstacles on either side of chkpt
        for point in self.lvl1ChkPts:
            self.createObs(point + Vector3(0, 0, 650))
            self.createObs(point - Vector3(0, 0, 250))

                
    def tick(self, dt):        
        for ent in self.entList:        
            ent.tick(dt)        
                
    def stop(self):        
        pass
