from vector import Vector3


class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"
        pass

    def init(self):
        self.loadLevel()


    def loadLevel(self):
        self.game1()
        

    def game1(self):
        x = 0
        for entType in self.engine.entityMgr.entTypes:
            print "GameMgr Creating", str(entType)
            ent = self.engine.entityMgr.createEnt(entType, pos = Vector3(0, 0, x))
            print "GameMgr Created: ", ent.uiname, ent.eid
            x += 400

        positionTemp = 0
        for z in range(0,10):
            obs = self.engine.entityMgr.createObs(pos = Vector3(positionTemp, 0, -200))
            obs = self.engine.entityMgr.createObs(pos = Vector3(positionTemp, 0, 600))
            positionTemp += 100


    def tick(self, dt):
        pass

    def stop(self):
        pass
        

