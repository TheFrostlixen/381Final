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
        self.overlayList.append(ScoreOverlay(self.engine, self.overlayManager))
        
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
        
        #create panel for first place
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_First_Panel")
        panel.setPosition(0.1, 0.8)
        panel.setDimensions(0.15, 0.04)
        
        #create first place text element
        first = self.overlayManager.createOverlayElement("TextArea", self.name+"_first")
        first.setMetricsMode(ogre.GMM_PIXELS)
        first.setPosition(100,950)
        first.setFontName("BlueHighway")
        first.setCharHeight(30)
        first.setColour(ogre.ColourValue(0,0,0))
        p1 = self.engine.entityMgr.entList[0].isSelected
        if p1:
            self.firstPlace = "Player 1"
        else:
            self.firstPlace = "Player 2"
            
        first.setCaption("1st:\n" + self.firstPlace)
        
        self.firstPanel = panel
        self.firstPanel.firstText = first
        
        self.panel.addChild(first)
        self.overlay.add2D(panel)
        
        #create panel for time
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Time_Panel")
        panel.setPosition(0.5, 0.5)
        panel.setDimensions(0.15, 0.04)
        
        #create time element
        time = self.overlayManager.createOverlayElement("TextArea", self.name+"_Time")
        time.setMetricsMode(ogre.GMM_PIXELS)
        time.setPosition(320,50)
        time.setFontName("BlueHighway")
        time.setCharHeight(40)
        time.setColour(ogre.ColourValue(1,1,1))
        self.curTime = 0.0
        time.setCaption("Time: " + "%.2f" % self.curTime)
        
        self.timePanel = panel
        self.timePanel.timeText = time
        
        self.panel.addChild(time)
        self.overlay.add2D(panel)
        


        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Level_Panel")
        panel.setPosition(0.3, 0.5)
        panel.setDimensions(0.15, 0.04)
        
        #create time element
        level = self.overlayManager.createOverlayElement("TextArea", self.name+"_Level")
        level.setMetricsMode(ogre.GMM_PIXELS)
        level.setPosition(650,980)
        level.setFontName("BlueHighway")
        level.setCharHeight(30)
        level.setColour(ogre.ColourValue(0,0,0))
        self.curLevel = 0.0
        level.setCaption("Level: " + "%d" % self.curLevel)
        
        self.levelPanel = panel
        self.levelPanel.levelText = level
        
        self.panel.addChild(level)
        self.overlay.add2D(panel)

    def tick(self, dtime):
        self.curTime += dtime
        self.timePanel.timeText.setCaption("Time: " + "%.2f" % self.curTime)
        
        p1 = self.engine.entityMgr.entList[0].isSelected
        if p1:
            self.firstPlace = "Player 1"
        else:
            self.firstPlace = "Player 2"
        
        self.firstPanel.firstText.setCaption("1st:\n" + self.firstPlace)
        self.levelPanel.levelText.setCaption("Level: " + "%d" % self.curLevel)
        self.panel.show()
        self.timePanel.show()
        self.levelPanel.show()

class ScoreOverlay(Overlay):
    name = "Score"
    
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)
        
        self.loadOverlay()
        
    def loadOverlay(self):
        #create panel for score background
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Panel")
        panel.setPosition(0.0,0.0)
        panel.setDimensions(1.0, 1.0)
        panel.setMaterialName("GUI_Background")
        
        self.panel = panel
        self.overlay.add2D(panel)
        
        #create panel for scores
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Score_Panel")
        panel.setPosition(0.5, 0.5)
        panel.setDimensions(0.15, 0.04)
        
        #create high score element
        score = self.overlayManager.createOverlayElement("TextArea", self.name+"_Scores")
        score.setMetricsMode(ogre.GMM_PIXELS)
        score.setPosition(50,60)
        score.setFontName("BlueHighway")
        score.setCharHeight(40)
        score.setColour(ogre.ColourValue(0,0,0))
        
        self.scoreString = ""
        for item in self.engine.scoreMgr.scoreList:
            self.scoreString += item[0] + ' ' + item[1] + ' ' + item[2] + ' ' + item[3] + ' ' + '\n'
        score.setCaption(self.scoreString)
        
        self.scorePanel = panel
        self.scorePanel.scoreText = score
        
        self.panel.addChild(score)
        self.overlay.add2D(self.scorePanel)
        
    def tick(self, dtime):
        #update scores so that they show correctly at the end
        self.scoreString = "            High Scores:\n\n\n"
        scoreNum = 1
        for score in self.engine.scoreMgr.scoreList:
            if scoreNum <= 10:
                self.scoreString += str(scoreNum) + ': ' + score[0] + ' ' + score[1] + ' ' + score[2] + ' ' + score[3] + ' ' + '\n'
                scoreNum += 1
        self.scoreString += "\n\nPlayer 1 Score: " + str(self.engine.scoreMgr.p1Time)
        self.scoreString += "\nPlayer 2 Score: " + str(self.engine.scoreMgr.p2Time)
        self.scorePanel.scoreText.setCaption(self.scoreString)
        self.panel.show()
        self.scorePanel.show()












