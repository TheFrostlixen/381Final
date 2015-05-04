#Sound Manager

"""
WONT WORK WITH MP3's, USE WAV's

"""

import os, pygame.mixer

class SoundMgr:
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        pygame.mixer.init(44100,-16,3,2048)

        self.totaltime = 0

        self.f1 = True
        self.f2 = True
        self.f3 = True
        
        self.a = os.path.join('data','Polyphia_Envision_Short.wav') # 1/8 = 220 milisecs
        self.b = os.path.join('data','Big_Blue.WAV')
        #self.c = os.path.join('data','Careless_Whisper.wav')

        self.aa = pygame.mixer.Sound(self.a)
        self.bb = pygame.mixer.Sound(self.b)
        #self.cc = pygame.mixer.Sound(self.c)

        self.aaa = pygame.mixer.Channel(0)
        self.bbb = pygame.mixer.Channel(1)
        #self.ccc = pygame.mixer.Chanell(2)
        print "SOUND INIT"


    def tick(self, dt):

        if self.totaltime == 0:
            print "Play Intro"
            self.aaa.set_volume(0.5)
            self.aaa.play(self.aa)

        if self.f1:
            if self.totaltime > 25:
                self.f1 = False
                self.aaa.fadeout(2000)
            if not self.engine.inputMgr.inputListener.mainMenu:
                self.f1 = False
                self.aaa.fadeout(200)


        if not self.f1 and self.f2 and not self.engine.inputMgr.inputListener.mainMenu:
            print "Play BB"
            self.f2 = False
            self.bbb.play(self.bb, loops = -1)

        #if self.f3:
            #if self.engine.selectionMgr.p1End or self.engine.selectionMgr.p2End:
                #print "Whisper....."
                #self.f3 = False
                #self.ccc.player(self.cc, loops = -1)


        self.totaltime += dt


    def stop(self):
        pygame.mixer.quit()
