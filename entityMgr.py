#Entity Manager		
from vector import Vector3		
		
class EntityMgr:		
    def __init__(self, engine):		
        print "starting entity manager"		
        self.engine = engine		
        		
    def init(self):		
        self.entList = []		
        self.numEnts = 0		
        		
        import ent		
        self.entTypes = [ent.Sleek, ent.Destroyer]		
        		
    def createEnt(self, entType, pos = Vector3(0,0,0)):		
        ent = entType(self.engine, self.numEnts, pos = pos)		
        ent.init()		
        self.entList.append(ent)		
        self.numEnts = self.numEnts + 1		
        return ent		
		
    def tick(self, dt):		
        for ent in self.entList:		
            ent.tick(dt)		
        		
    def stop(self):		
        pass