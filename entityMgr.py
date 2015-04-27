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
        self.numItem_Boost = 0        

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

    def createItem_Boost(self, pos = Vector3(0,0,0)):        
        item = ent.Item_Boost(self.engine, self.numItem_Boost, pos = pos)        
        item.init()
        item.uiname += str(self.numItem_Boost)
        self.lvl1List.append(item)        
        self.numItem_Boost = self.numItem_Boost + 1        
        return item
        
    def createLvl1(self):
        """#create chkpt list
        for i in xrange(0,100):
            vector = Vector3(i * 100,0,0)
            self.lvl1ChkPts.append(vector)
            
        #create obstacles on either side of chkpt
        for point in self.lvl1ChkPts:
            self.createObs(point + Vector3(0, 0, 650))
            self.createObs(point + Vector3(0, 0, -250))

        #create item boost
        self.createItem_Boost(Vector3(5000, 50, 150))
        """
        #create first leg
        for i in xrange(0,100):
            vector = Vector3(i * 100,0,0)
            self.lvl1ChkPts.append(vector)
            self.createObs(vector + Vector3(0,0,650))
            self.createObs(vector + Vector3(0,0, -250))
        #make turn's right edge
        for i in xrange(0,13):
            vector = Vector3(100 + self.lvl1ChkPts[-1].x, 0, 0)
            self.createObs(vector + Vector3(0,0,650))
            if i < 7:
                self.lvl1ChkPts.append(vector)
                
        #make turn's top edge
        nextX = self.lvl1ChkPts[-1].x
        turnPoint = self.lvl1ChkPts[-1]
        for i in xrange(0,24):
            vector = Vector3(nextX, 0, self.lvl1ChkPts[-1].z - 100)
            self.createObs(vector + Vector3(200,0,650))
            if i < 11:
                self.lvl1ChkPts.append(vector)
            
        #make turn's bottom edge
        nextX = turnPoint.x
        for i in xrange(0,14):
            vector = Vector3(nextX, 0, turnPoint.z - (100*i))
            self.createObs(vector + Vector3(-650, 0, -250))
            
        #make return right edge
        for item in self.lvl1ChkPts:
            self.createItem_Boost(item)
        
            
    def tick(self, dt):        
        for ent in self.entList:        
            ent.tick(dt)        
                
    def stop(self):        
        pass
        
        
        
        
        
        
        
        
        
        
        
        
