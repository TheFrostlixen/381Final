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
		
    def tick(self, dt):		
        for ent in self.entList:		
            ent.tick(dt)		
        		
    def stop(self):		
        pass