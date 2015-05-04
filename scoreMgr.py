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
                
    def init(self): 
        self.scoreList = []

        with open('HighScores') as file:
            for line in file:
                self.scoreList.append(int(line))
                print(int(line))

    def addCurrentTime(self):
        self.scoreList.append(int(self.engine.overlayMgr.overlayList[1].curTime))
        self.scoreList.sort()
            
    def tick(self, dt):   
        pass     
                
    def stop(self):        
        file = open('HighScores', 'w')
        for x in self.scoreList:
            file.write('%d \n' % x)
        file.close
        
        
        
        
        
        
        
        
        
        
