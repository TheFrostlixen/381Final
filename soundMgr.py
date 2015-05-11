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
        self.c = os.path.join('data','Careless_Whisper.WAV')
        self.d = os.path.join('data','Boat_Boost.WAV')
        self.e = os.path.join('data','Rocket_Equip.WAV')
        self.f = os.path.join('data','Rocket_Explosion.WAV')
        self.g = os.path.join('data','Rocket_Zoom.WAV')
        self.h = os.path.join('data','Thud.WAV')

        self.Polyphia_Envision_Short = pygame.mixer.Sound(self.a)
        self.Big_Blue = pygame.mixer.Sound(self.b)
        self.Careless_Whisper = pygame.mixer.Sound(self.c)
        self.Boat_Boost = pygame.mixer.Sound(self.d)
        self.Rocket_Equip = pygame.mixer.Sound(self.e)
        self.Rocket_Explosion = pygame.mixer.Sound(self.f)
        self.Rocket_Zoom = pygame.mixer.Sound(self.g)
        self.Thud = pygame.mixer.Sound(self.h)


        self.IntroSong = pygame.mixer.Channel(0)
        self.Playlist = pygame.mixer.Channel(1) 
        self.SoundFX = pygame.mixer.Channel(2)
        print "SOUND INIT"


    def tick(self, dt):

        if self.totaltime == 0:
            print "Play Intro"
            self.IntroSong.stop()
            self.IntroSong.set_volume(0.5)
            self.IntroSong.play(self.Polyphia_Envision_Short)

        self.totaltime += dt

        if self.f1:
            if self.totaltime > 25:
                self.IntroSong.fadeout(2000)
            if self.totaltime > 27:
                print "hello", self.totaltime
                self.totaltime = 0
                print self.totaltime
            if not self.engine.inputMgr.inputListener.mainMenu:
                self.f1 = False
                self.IntroSong.fadeout(200)


        #if not self.f1 and self.f2 and not self.engine.inputMgr.inputListener.mainMenu:
            #print "Play BB"
            #self.f2 = False
            #self.Playlist.play(self.Big_Blue, loops = -1)

        if self.f3:
            if (self.engine.selectionMgr.p1End and not self.engine.selectionMgr.p2End) or (self.engine.selectionMgr.p2End and not self.engine.selectionMgr.p1End):
                self.f3 = False
                self.play_Whisper()



    def stop(self):
        pygame.mixer.quit()

    def play_Whisper(self):
        self.Playlist.stop()
        self.Playlist.play(self.Careless_Whisper, loops = -1)

    def play_Big_Blue(self):
        self.Playlist.stop()
        self.Playlist.play(self.Big_Blue, loops = -1)


    def sBoat_Boost(self):
        self.SoundFX.play(self.Boat_Boost)

    def sRocket_Equip(self):
        self.SoundFX.play(self.Rocket_Equip)

    def sRocket_Explosion(self):
        self.SoundFX.play(self.Rocket_Explosion)

    def sRocket_Zoom(self):
        self.SoundFX.play(self.Rocket_Zoom)

    def sThud(self):
        self.SoundFX.play(self.Thud)



