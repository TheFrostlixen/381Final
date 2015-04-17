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
        for line in xrange(0,4):
            if line == 0:
                for coord in xrange(0,40):
                    vector = Vector3(coord*100,0,0)
                    self.lvl1ChkPts.append(vector)
                    self.createObs(vector + Vector3(0,0,200))
                    self.createObs(vector - Vector3(0,0,200))
                    
            elif line == 1:
                for coord in xrange(0,40):
                    vector = Vector3(4000,0,coord * -1 * 100)
                    self.lvl1ChkPts.append(vector)
                    self.createObs(vector + Vector3(200,0,0))
                    self.createObs(vector - Vector3(200,0,0))
            
            elif line == 2:
                for coord in xrange(0,40):
                    vector = Vector3(4000 - (coord*100),0,-4000)
                    self.lvl1ChkPts.append(vector)
                    self.createObs(vector + Vector3(0,0,200))
                    self.createObs(vector - Vector3(0,0,200))
            
            elif line == 3:
                for coord in xrange(0,40):
                    vector = Vector3(0,0,-4000 + (coord * 100))
                    self.lvl1ChkPts.append(vector)
                    self.createObs(vector + Vector3(200,0,0))
                    self.createObs(vector - Vector3(200,0,0))

                
    def tick(self, dt):        
        for ent in self.entList:        
            ent.tick(dt)        
                
    def stop(self):        
        pass
