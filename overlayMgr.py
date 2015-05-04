import ogre.renderer.OGRE as ogre
import math

class OverlayMgr:
    def __init__(self, engine):
        self.engine = engine
        
    def init(self):
        self.overlayManager = ogre.OverlayManager.getSingleton()
        
        self.selection = 0
        self.showIntroPage = False
        
        self.overlayList = []
        self.loadOverlays()
        self.currentOverlay = ""
        self.setOverlay("Start")
        
    def loadOverlays(self):
        self.overlayList.append(StartOverlay(self.engine, self.overlayManager))
        self.overlayList.append(GameOverlay(self.engine, self.overlayManager))
        
    def setOverlay(self, name):
        self.currentOverlay = name
        for overlay in self.overlayList:
            overlay.setVisible(overlay.name == name)
                
    def getOverlayByName(self, name):
        for overlay in self.overlayList:
            if overlay.name == self.currentOverlay:
                return overlay
                
    def tick(self, dtime):
        for overlay in self.overlayList:
            if overlay.name == self.currentOverlay:
                overlay.tick(dtime)
                
class Overlay:
    def __init__(self, engine, overlayManager, name):
        self.engine = engine
        
        self.name = name
        self.overlayManager = overlayManager
        self.overlay = self.overlayManager.create(self.name + "Overlay")
        
    def setVisible(self, isVisible):
        if isVisible:
            self.overlay.show()
        else:
            self.overlay.hide()
            
class StartOverlay(Overlay):
    name = "Start"
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)
        
        self.loadOverlay()
        
    def loadOverlay(self):
        #Create start menu logo
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Logo")
        panel.setPosition(0.1, 0.1)
        panel.setDimensions(0.8, 0.8)
        panel.setMaterialName("Splash_Logo")
        
        self.logo = panel
        
        self.overlay.add2D(panel)
        
        #Create Start Button
        
        panel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_Start_Button")
        panel.setPosition(0.45, 0.75)
        panel.setDimensions(0.12, 0.08)
        panel.setMaterialName("Splash_Start_Button")
        panel.setBorderMaterialName("GUI_Grey_Border")
        panel.setBorderSize(0.003)
        
        self.playButton = panel
        
        self.overlay.add2D(panel)
        
        #Create About/Intro Button
        
        panel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_Intro_Button")
        panel.setPosition(0.45, 0.60)
        panel.setDimensions(0.12, 0.08)
        panel.setMaterialName("Splash_About_Button")
        panel.setBorderMaterialName("GUI_Grey_Border")
        panel.setBorderSize(0.003)
        
        self.introButton = panel
        
        self.overlay.add2D(panel)
        #Create About/Intro Panel
        
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Intro")
        panel.setPosition(0.1, 0.1)
        panel.setDimensions(0.8, 0.8)
        panel.setMaterialName("Splash_About")
        
        self.intro = panel
        
        self.overlay.add2D(panel)
        
    def tick(self, dtime):
        if self.engine.overlayMgr.selection == 1:
            self.playButton.setBorderMaterialName("GUI_Grey_Border")
            self.introButton.setBorderMaterialName("GUI_Red_Border")
        else:
            self.playButton.setBorderMaterialName("GUI_Red_Border")
            self.introButton.setBorderMaterialName("GUI_Grey_Border")
            
        if self.engine.overlayMgr.showIntroPage:
            self.playButton.hide()
            self.introButton.hide()
            self.logo.hide()
            self.intro.show()
        else:
            self.playButton.show()
            self.introButton.show()
            self.logo.show()
            self.intro.hide()
        
        
class GameOverlay(Overlay):
    name = "Game"
    
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)
        
        self.loadOverlay()
        
    def loadOverlay(self):
        #create panel for hud background
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Panel")
        panel.setPosition(0.0,0.0)
        panel.setDimensions(1.0, 1.0)
        panel.setMaterialName("GUI_Background")
        
        self.panel = panel
        self.overlay.add2D(panel)
        
        #create panel for time
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Time_Panel")
        panel.setPosition(0.45, 0.02)
        panel.setDimensions(0.15, 0.04)
        
        #create time element
        time = self.overlayManager.createOverlayElement("TextArea", self.name+"_Time")
        time.setMetricsMode(ogre.GMM_PIXELS)
        time.setFontName("BlueHighway")
        time.setCharHeight(20)
        time.setColour(ogre.ColourValue(1,1,1))
        self.curTime = 0.0
        time.setCaption("%.2f" % self.curTime)
        
        self.timePanel = panel
        self.timePanel.timeText = time
        
        self.panel.addChild(time)
        self.overlay.add2D(panel)

    def tick(self, dtime):
        self.curTime += dtime
        self.timePanel.timeText.setCaption("%.2f" % self.curTime)
        self.panel.show()
        self.timePanel.show()














