#Sound Manager

"""
WONT WORK WITH MP3's, USE WAV's

"""

import os, pygame.mixer

class SoundMgr:
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        pygame.mixer.init(44100,-16,2,2048)

        self.totaltime = 0

        self.f1 = 0
        self.f2 = 0
        
        self.a = os.path.join('data','Polyphia_Envision_Short.wav') # 1/8 = 220 milisecs
        self.b = os.path.join('data','Polyphia_Envision.wav')

        self.aa = pygame.mixer.Sound(self.a)
        self.bb = pygame.mixer.Sound(self.b)

        self.aaa = pygame.mixer.Channel(0)
        self.bbb = pygame.mixer.Channel(1)
        print "SOUND INIT"


    def tick(self, dt):

        if self.totaltime == 0:
            print "WE GOOD"
            self.aaa.play(self.aa)
            #self.bbb.play(self.bb)

        if self.totaltime == 3000:
            self.aaa.fadeout(2000)

        self.totaltime += 2


    def stop(self):
        pygame.mixer.quit()
