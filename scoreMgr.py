#Entity Manager
import os.path        
import datetime
from vector import Vector3
import ent     
import random
  
class ScoreMgr:        
    """    def __init__(self, engine):        
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
    """
    def __init__(self, engine):
        print "starting score manager"
        self.engine = engine
    
    def init(self):
        self.scoreList = []
        self.scoreNum = 0
        currentscore = []
        curPiece = 1
        if os.path.isfile('HighScores'):
            with open('HighScores', 'r') as scoreFile:
                for piece in self.readByTokens(scoreFile):
                    if curPiece < 4:
                        #get piece 1, 2, then 3
                        currentscore.append(piece)
                        curPiece += 1
                    elif curPiece == 4:
                        #get fourth piece, add to list, reset curPiece
                        currentscore.append(piece)
                        self.scoreList.append(currentscore)
                        currentscore = []
                        curPiece = 1
                    else:
                        curPiece = 1
        else:
            #highscores does not exist
            pass
        
        
    def tick(self, dt):
        pass
        
    def addCurrentTime(self, player):
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        realtime = datetime.datetime.now().strftime("%I:%M%p")
        currentscore = []
        currentscore.append(str(self.engine.overlayMgr.overlayList[1].curTime))
        currentscore.append(player)
        currentscore.append(date)
        currentscore.append(realtime)
        self.scoreList.append(currentscore)
        self.scoreNum += 1
        self.scoreList.sort(key=lambda x: float(x[0]))

    def stop(self):
        file = open('HighScores', 'w')
        counter = 0
        for score in self.scoreList:
            if counter < 10:
                file.write(score[0] + ' ' + score[1] + ' ' + score[2] + ' ' + score[3] + ' ' + '\n')
            counter += 1
        file.close()
        
    def printScoreList(self):
        for score in self.scoreList:
            print score[0] + ' ' + score[1] + ' ' + score[2] + ' ' + score[3]
            
    def readByTokens(self, fileobj):
        for line in fileobj:
            for token in line.split():
                yield token
        
        
        
        
        
