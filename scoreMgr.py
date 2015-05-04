#Entity Manager        
import time
from datetime import date
from vector import Vector3    
import ent     
import random
  
class ScoreMgr:        
    def __init__(self, engine):        
        print "starting score Manger"        
        self.engine = engine
        self.currentRun = 0        
                
    def init(self): 
        self.scoreList = []

        with open('HighScores') as file:
            line_value = file.readline(100).strip()
            if len(line_value) > 0:
                print line_value
                line_value = int(line_value)
            self.currentRun = int(line_value)
            print self.currentRun
            for line in file:
                self.scoreList.append([int(x) for x in line.split()])
            print(self.scoreList)
            self.currentRun += 1

    def addCurrentTime(self):
        self.scoreList.append((self.currentRun, int(self.engine.overlayMgr.overlayList[1].curTime)))
        self.scoreList.sort()
            
    def tick(self, dt):   
        pass     
                
    def stop(self):        
        file = open('HighScores', 'w')
        file.write('%d \n' % self.currentRun)
        for (x, y) in self.scoreList:
            file.write('%d %d \n' % (x,y))
        file.close
        
        
        
        
        
        
        
        
        
        
