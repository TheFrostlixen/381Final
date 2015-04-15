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
            obs = self.engine.entityMgr.createObs(pos = Vector3(positionTemp, 0, -600))
            obs = self.engine.entityMgr.createObs(pos = Vector3(positionTemp, 0, -1000))
            positionTemp += 100

        #positionTemp = 0
        #for z in range(0,5):

        #create right bend
        #interior
        obs = self.engine.entityMgr.createObs(pos = Vector3(1000, 0, -200))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1100, 0, -300))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1200, 0, -400))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1100, 0, -500))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1000, 0, -600))
        #exterior
        obs = self.engine.entityMgr.createObs(pos = Vector3(1000, 0, 500))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1100, 0, 400))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1200, 0, 300))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1300, 0, 200))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1400, 0, 100))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1500, 0, 000))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1600, 0, -100))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1600, 0, -200))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1600, 0, -300))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1600, 0, -400))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1600, 0, -500))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1500, 0, -600))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1400, 0, -700))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1300, 0, -800))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1200, 0, -900))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1100, 0, -1000))
        obs = self.engine.entityMgr.createObs(pos = Vector3(1000, 0, -1000))


    def tick(self, dt):
        pass

    def stop(self):
        pass
        

