#selection manager

import ogre.io.OIS as OIS
#import ogre.sound.OgreAL as OgreAL

class SelectionMgr:
    def __init__(self, engine):
        self.engine = engine
        self.musicVolume = 1.0
        self.soundmanager = None
        self.entSound = None

    def init(self):
        self.selectedEnts = []
        self.selectedEntIndex = self.engine.entityMgr.numEnts;
        self.selectedEnt = None
        self.keyboard = self.engine.inputMgr.keyboard
        self.camera = self.engine.gfxMgr.camera
        self.toggle = 0.3
        self.stopped = False
        
    def tick(self, dt):

        if self.stopped == True:
            return
            
        self.keyboard.capture()
        if self.toggle >= 0:
            self.toggle -= dt
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_TAB):
            self.toggle = 0.3
            if self.keyboard.isKeyDown(OIS.KC_LSHIFT):
                self.addNext()
            else:
                self.selectNext()
            

    def stop(self):
        self.stopped = True
        self.selectedEnt = None
        self.selectedEnts = []
        self.selectedEntIndex = -1
        
        
#------------------------------------------------------------------------------------#
        
        
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


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        




