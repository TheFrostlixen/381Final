#selection manager

import ogre.io.OIS as OIS
import math
#import ogre.sound.OgreAL as OgreAL

class SelectionMgr:
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.selectedEnts = []
        self.selectedEntIndex = self.engine.entityMgr.numEnts;
        self.selectedEnt = None
        self.keyboard = self.engine.inputMgr.keyboard
        self.camera = self.engine.gfxMgr.camera_P1
        self.toggle = 0.3
        self.stopped = False
        self.entMgr = self.engine.entityMgr
        
    def tick(self, dt):

        if self.stopped == True:
            return
        
        #get nearest checkpoint to each player
        p1 = self.getNearestPoint(self.entMgr.entList[0])
        p2 = self.getNearestPoint(self.entMgr.entList[1])
        #compare checkpoint
        if p1 == len(self.entMgr.lvl1ChkPts) - 1:
            #player 1 wins
            print "Player 1 Wins!"
            self.engine.stop()
            return
        elif p2 == len(self.entMgr.lvl1ChkPts) - 1:
            #player 2 wins
            print "Player 2 Wins!"
            self.engine.stop()
            return
        elif p1 == p2:
            #compare closeness to next checkpoint if they are equal
            d1 = self.getDistanceTo(self.entMgr.lvl1ChkPts[p1] + 1, self.entMgr.entList[0])
            d2 = self.getDistanceTo(self.entMgr.lvl1ChkPts[p2] + 1, self.entMgr.entList[1])
            if d1 <= d2:
                first = self.entMgr.entList[0]
            else:
                first = self.entMgr.entList[1]
        elif p1 > p2:
            first = self.entMgr.entList[0]
        else:
            first = self.entMgr.entList[1]
            
        #draw box of player who is closest to the farthest checkpoint
        self.updateCurrentSelection(False)
        self.addSelected(first)

    def stop(self):
        self.stopped = True
        self.selectedEnt = None
        self.selectedEnts = []
        self.selectedEntIndex = -1
        
        
#------------------------------------------------------------------------------------#
        
    def getNearestPoint(self, ent):
        nearest = 100000000000
        index = 0
        for point in xrange(0,len(self.entMgr.lvl1ChkPts)):
            dist = self.getDistanceTo(self.entMgr.lvl1ChkPts[point], ent)
            if dist <= nearest:
                nearest = dist
                index = point
        return index
    
    def getDistanceTo(self, point, ent):
        posX = ent.pos.x
        posZ = ent.pos.z
        xDiff = point.x - posX
        zDiff = point.z - posZ
        
        dist = math.sqrt(math.pow(xDiff, 2) + math.pow(zDiff, 2))
        
        return dist
    
    
    def updateCurrentSelection(self, isSelected):
        for ent in self.selectedEnts:
            ent.isSelected = isSelected
        if not isSelected:
            self.selectedEnts = []
            
    def selectEnt(self, ent):
        self.updateCurrentSelection(False)
        self.selectedEnts = []
        self.addSelected(ent)
        #self.entSound = self.soundmanager.createSound(ent.eid, ent.sound, True)
        #self.entSound.play()
        
    def addSelected(self, ent):
        self.selectedEnt = ent
        self.selectedEnts.append(ent)
        self.selectedEntIndex = ent.eid
        self.selectedEnt.isSelected = True
        
        
    def clearSelection(self):
        self.updateCurrentSelection(False)
    
    def selectNext(self):
        self.selectedEntIndex = self.getNextSelectedEntIndex(self.selectedEntIndex)
        self.selectEnt(self.engine.entityMgr.entList[self.selectedEntIndex])
        return
        
    def addNext(self):
        self.selectedEntIndex = self.getNextSelectedEntIndex(self.selectedEntIndex)
        self.addSelected(self.engine.entityMgr.entList[self.selectedEntIndex])
        return
        
    def getNextSelectedEntIndex(self, index):
        if index >= self.engine.entityMgr.numEnts - 1:
            index = 0
        else:
            index = index + 1
        return index
        
    def getPrimarySelection(self):
        return self.selectedEnts[0]


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        




