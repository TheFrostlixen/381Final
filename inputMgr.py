#Andrew Menard and Brian Gaunt
#CS 381
#Input Manager

"""
    USE TUTORIAL #5
"""
import pygame
from pygame.locals import *
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math

# class JoyEvent:
#     BUTTON_PRESSED  = 0
#     BUTTON_RELEASED = 1
#     AXIS_MOVED      = 2
#     POV_MOVED       = 3
#     VECTOR3_MOVED   = 4
#     NUM             = 5
#     INVALID         = 6

# class JoyButtons: # XBox Controller, the buttons need to be checked
#     BACK       = 0
#     A          = 1
#     B          = 2
#     X          = 3
#     Y          = 4
#     LEFT       = 5
#     RIGHT      = 6
#     START      = 7
#     XBOX       = 8
#     LEFT_AXIS  = 9
#     RIGHT_AXIS = 10
#     POV        = 11

#     NUM     = 12
#     LIST    = [BACK, A, B, X, Y, LEFT, RIGHT, START, XBOX, LEFT_AXIS, RIGHT_AXIS, POV]

# class JoyAxes: # XBox Controller
#     LEFT_LEFTRIGHT    = 0
#     LEFT_UPDOWN       = 1
#     LEFT_LEFT         = 2
#     RIGHT_LEFTRIGHT   = 3
#     RIGHT_UPDOWN      = 4
#     RIGHT_RIGHT       = 5
#     NUM               = 6

#     LIST    = [LEFT_LEFTRIGHT, LEFT_UPDOWN, LEFT_LEFT, RIGHT_LEFTRIGHT, RIGHT_UPDOWN, RIGHT_RIGHT]

class InputMgr():

    def __init__(self, engine):
        self.engine = engine
    
    def init(self):

        self.root = self.engine.gfxMgr.root
        self.keepRendering = True
        pygame.init()
        self.joysticks = []
        self.p1LR = 0;
        self.p2LR = 0;
        
        self.joystick_count = pygame.joystick.get_count()
        print self.joystick_count
        print "ASDF"
        for i in range(0, pygame.joystick.get_count()):
            # create an Joystick object in our list
            self.joysticks.append(pygame.joystick.Joystick(i))
            # initialize them all (-1 means loop forever)
            self.joysticks[-1].init()
            # print a statement telling what the name of the controller is
            print "Detected joystick '",self.joysticks[-1].get_name(),"'"

        import platform
        int64 = False
        for bit in platform.architecture():
            if '64' in bit:
                int64 = True
        windowHandle = 0
        renderWindow = self.root.getAutoCreatedWindow()
        if int64:
            windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        else:
            windowHandle = renderWindow.getCustomAttributeInt("WINDOW")

        paramList = [("WINDOW", str(windowHandle))]

        t = [("x11_mouse_grab", "true"), ("x11_mouse_hide", "false")]
        paramList.extend(t)
        

        self.inputManager = OIS.createPythonInputSystem(paramList)
        #This sets up the InputManager for use, but to actually use OIS to get input for the
        #keyboard and mouse, you'll need to create the following objects
        # try:
        #     self.joystick = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, True)
        #     print "----------------------------------->Made joystick object"
        # except Exception, e:     self.joystick = None
        #     print "----------------------------------->No Joy, Don't Worry Be Happy"
        #     print "----------------------------------->Who uses joysticks anyways? - so 1995"
        # if self.joystick:
        #     self.jMgr = JoyStickListener(self)

        # try:
        #     self.joy2stick = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, True)
        #     print "----------------------------------->Made joystick object"
        # except Exception, e:
        #     self.joy2stick = None
        #     print "----------------------------------->No Joy, Don't Worry Be Happy"
        #     print "----------------------------------->Who uses joysticks anyways? - so 1995"
        # if self.joy2stick:
        #     self.jMgr2 = Joy2StickListener(self)

        self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
        # self.jMgr2 = Joy2StickListener(self)
        # self.jMgr = JoyStickListener(self)
        self.createFrameListener()

    def createFrameListener(self):
        self.exitListener = ExitListener(self)
        self.root.addFrameListener(self.exitListener)
        self.inputListener = InputListener(self)
        self.root.addFrameListener(self.inputListener)
    
    def tick(self, dt):
        # if self.joystick:
        #     self.joystick.capture()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.JOYAXISMOTION:
                pass
                #print "Joystick '",self.joysticks[event.joy].get_name()," ", event.joy, " ", "' axis",event.axis,"motion."
        
        if pygame.joystick.get_count() > 0:
            p1LR = self.joysticks[0].get_axis(0)
        if pygame.joystick.get_count() > 1:
            p2LR = self.joysticks[1].get_axis(0)

        print self.joysticks[0].get_axis(4)
        print self.joysticks[0].get_axis(5)

        if (self.engine.keepRunning == False):
            self.engine.stop()

    
    def stop(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None

class InputListener(ogre.FrameListener):
    def __init__(self, inputMgr):
        ogre.FrameListener.__init__(self)
        self.inputMgr = inputMgr
        self.keyboard = self.inputMgr.keyboard
        self.cameraMgr = self.inputMgr.engine.cameraMgr
        self.sceneManager = self.inputMgr.engine.gfxMgr.sceneManager

        self.toggle = 0
        self.timer_MainMenu = 0
        self.mainMenu = True

        self.keepRendering = self.inputMgr.keepRendering

    def frameStarted(self, frameEvent):
        self.keyboard.capture()

        #process unbuffered key input for Escape
        self.keyPressed(frameEvent)

        self.timer_MainMenu += frameEvent.timeSinceLastFrame

        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame
        
        if self.mainMenu:
            self.cameraMgr.start_MainMenu()

        if self.mainMenu and self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_RETURN):
            self.toggle = 0.1
            self.mainMenu = False
            self.cameraMgr.end_MainMenu()


        #check for Key release to stop moving the camera.
        self.keyReleased(frameEvent)

        return True


    def keyPressed(self, frameEvent):

        if self.keyboard.isKeyDown(OIS.KC_LEFT) or self.inputMgr.joysticks[0].get_axis(0) < -0.6:
            self.cameraMgr.P1_CamTurn_Left()
                    
        if self.keyboard.isKeyDown(OIS.KC_RIGHT) or self.inputMgr.joysticks[0].get_axis(0) > 0.6:
            self.cameraMgr.P1_CamTurn_Right()

        if self.keyboard.isKeyDown(OIS.KC_NUMPAD4) or self.inputMgr.joysticks[1].get_axis(0) < -0.6:
            self.cameraMgr.P2_CamTurn_Left()
                    
        if self.keyboard.isKeyDown(OIS.KC_NUMPAD6) or self.inputMgr.joysticks[0].get_axis(0) > 0.6:
            self.cameraMgr.P2_CamTurn_Right()

        return True

    def keyReleased(self, frameEvent):
        return True


class ExitListener(ogre.FrameListener):

    def __init__(self, inputMgr):
        ogre.FrameListener.__init__(self)
        self.inputMgr = inputMgr
        self.keyboard = self.inputMgr.keyboard
 
    def frameStarted(self, frameEvent):
        self.keyboard.capture()

        #process unbuffered key input for Escape
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.inputMgr.keepRendering = False

        return self.inputMgr.keepRendering

    def __del__(self):
        del self.inputListener
        del self.exitListener
        del self.root
       
class JoyStickListener(OIS.JoyStickListener):
    def __init__(self, inputMgr):
        OIS.JoyStickListener.__init__(self)
        self.inputMgr = inputMgr
        self.engine = self.inputMgr.engine
        self.joystick = self.inputMgr.joystick
        self.triggerRDown = False
        self.triggerLDown = False
        self.joyLDown = False
        self.joyRDown = False
        self.joyLUp = False
        self.joyRUp = False
        if self.joystick:
            self.joystick.setEventCallback(self)
            self.ms = self.joystick.getJoyStickState()
            self.joyHandlers = [dict() for x in range(JoyEvent.NUM)]
            self.player2 = self.engine.entityMgr.entList[1]

    def buttonPressed(self, frameEvent, button):
        print "------------------------------------>", " Button Pressed: ", button    
        self.callJoyHandlers(JoyEvent.BUTTON_PRESSED, button, frameEvent.get_state())    
        return True

    def buttonReleased(self, frameEvent, button):
        print "------------------------------------>",  " Button Released: ", button
        self.callJoyHandlers(JoyEvent.BUTTON_RELEASED, button, frameEvent.get_state())
        if button == 1:
            nextAccel = self.player2.speed + self.player2.acceleration
            if nextAccel < self.player2.maxSpeed:
                self.player2.desiredSpeed += self.player2.acceleration
        if button == 2:
            nextDecel = player2.speed - player2.acceleration
            if nextDecel > (-1*player2.maxSpeed/2):
                player2.desiredSpeed -= player2.acceleration
        return True

    def axisMoved(self, frameEvent, axis):
        state = frameEvent.get_state()
        if state.mAxes[axis].abs > 5000 or state.mAxes[axis].abs < - 5000 :
            self.callJoyHandlers(JoyEvent.AXIS_MOVED, axis, state)            
            #print "------------------------------------>",  " Axis  : ", axis, state.mAxes[axis].abs
        #right trigger down
        if axis == 5 and state.mAxes[axis].abs > 15000:
            self.triggerRDown = True
            print "--------------> trigger right down"
        #right trigger up
        if axis == 5 and state.mAxes[axis].abs < 15000:
            self.triggerRDown = False
            print "--------------> trigger right up"
        #left trigger down
        if axis == 2 and state.mAxes[axis].abs > 15000:
            self.triggerLDown = True 
        #left trigger up
        if axis == 2 and state.mAxes[axis].abs < 15000:
            self.triggerLDown = False 
        if axis == 0 and state.mAxes[axis].abs < -15000:
            self.joyLDown = True
        if axis == 0 and state.mAxes[axis].abs > -15000:
            self.joyLDown = False    
        if axis == 0 and state.mAxes[axis].abs > 15000:   
           self.joyRDown = True          
        if axis == 0 and state.mAxes[axis].abs < 15000:   
           self.joyRDown = False         
        return True

    def povMoved(self, frameEvent, povid):
        state = frameEvent.get_state()
        self.callJoyHandlers(JoyEvent.POV_MOVED, povid, state)            
        #print "------------------------------------>",  povid, state.mPOV[povid].direction
        return True

    def registerJoyHandler(self, event, joyButton, func):# func takes OIS.JoyEvent JoyState as arg
        self.joyHandlers[event].setdefault(joyButton, list())
        self.joyHandlers[event][joyButton].append(func)

    def callJoyHandlers(self, event, joyButton, js):
        self.joyHandlers[event].setdefault(joyButton, list())
        for handler in self.joyHandlers[event][joyButton]:
            handler(js)
    def joystickMoved(self, evt):
        pass

    def joystickPressed(self, evt, id):

        if id == OIS.MB_Left:
            self.leftDown = True
            self.ms = self.joystick.getJoyStickState()
            print self.ms.X.abs, self.ms.Y.abs
            joystickRay = self.camera.getCameraToViewportRay((self.ms.X.abs + 50) / float(evt.get_state().width), (self.ms.Y.abs + 25) / float(evt.get_state().height))
            self.raySceneQuery.setRay(joystickRay)
            result = self.raySceneQuery.execute()
            if len(result) > 2:
                    if result[2].movable:
                        print result[2].movable.getName()
                        for ent in self.inputMgr.engine.entityMgr.entList:
                            if (ent.uiname + str(ent.eid)) == result[2].movable.getName():
                                if self.inputMgr.keyboard.isKeyDown(OIS.KC_LSHIFT):
                                    self.inputMgr.engine.selectionMgr.addSelected(ent)
                                else:
                                    self.inputMgr.engine.selectionMgr.selectEnt(ent)
                                

        if id == OIS.MB_Right:
            self.rightDown = True

    def joystickReleased(self, evt, id):
        if id == OIS.MB_Left:
            self.leftDown = False
        if id == OIS.MB_Right:
            self.rightDown = False

class Joy2StickListener(OIS.JoyStickListener):
    def __init__(self, inputMgr):
        OIS.JoyStickListener.__init__(self)
        self.inputMgr = inputMgr
        self.engine = self.inputMgr.engine
        self.joy2stick = self.inputMgr.joy2stick
        self.triggerRDown = False
        self.triggerLDown = False
        self.joy2LDown = False
        self.joy2RDown = False
        self.joy2LUp = False
        self.joy2RUp = False
        if self.joy2stick:
            self.joy2stick.setEventCallback(self)
            self.ms = self.joy2stick.getJoyStickState()
            self.joy2Handlers = [dict() for x in range(JoyEvent.NUM)]
            self.player2 = self.engine.entityMgr.entList[0]

    def buttonPressed(self, frameEvent, button):
        print "------------------------------------>", " Button Pressed: ", button    
        self.calljoy2Handlers(joy2Event.BUTTON_PRESSED, button, frameEvent.get_state())    
        return True

    def buttonReleased(self, frameEvent, button):
        print "------------------------------------>",  " Button Released: ", button
        self.calljoy2Handlers(joy2Event.BUTTON_RELEASED, button, frameEvent.get_state())
        if button == 1:
            nextAccel = self.player2.speed + self.player2.acceleration
            if nextAccel < self.player2.maxSpeed:
                self.player2.desiredSpeed += self.player2.acceleration
        if button == 2:
            nextDecel = player2.speed - player2.acceleration
            if nextDecel > (-1*player2.maxSpeed/2):
                player2.desiredSpeed -= player2.acceleration
        return True

    def axisMoved(self, frameEvent, axis):
        state = frameEvent.get_state()
        if state.mAxes[axis].abs > 5000 or state.mAxes[axis].abs < - 5000 :
            self.calljoy2Handlers(joy2Event.AXIS_MOVED, axis, state)            
            print "------------------------------------>",  " Axis  : ", axis, state.mAxes[axis].abs
        #right trigger down
        if axis == 5 and state.mAxes[axis].abs > 15000:
            self.trigger2RDown = True
            print "--------------> trigger right down"
        #right trigger up
        if axis == 5 and state.mAxes[axis].abs < 15000:
            self.trigger2RDown = False
            print "--------------> trigger right up"
        #left trigger down
        if axis == 2 and state.mAxes[axis].abs > 15000:
            self.trigger2LDown = True 
        #left trigger up
        if axis == 2 and state.mAxes[axis].abs < 15000:
            self.trigger2LDown = False 
        if axis == 0 and state.mAxes[axis].abs < -15000:
            self.joy2LDown = True
        if axis == 0 and state.mAxes[axis].abs > -15000:
            self.joy2LDown = False    
        if axis == 0 and state.mAxes[axis].abs > 15000:   
           self.joy2RDown = True          
        if axis == 0 and state.mAxes[axis].abs < 15000:   
           self.joy2RDown = False         
        return True

    def povMoved(self, frameEvent, povid):
        state = frameEvent.get_state()
        self.calljoy2Handlers(joy2Event.POV_MOVED, povid, state)            
        #print "------------------------------------>",  povid, state.mPOV[povid].direction
        return True

    def registerjoy2Handler(self, event, joy2Button, func):# func takes OIS.joy2Event joy2State as arg
        self.joy2Handlers[event].setdefault(joy2Button, list())
        self.joy2Handlers[event][joy2Button].append(func)

    def calljoy2Handlers(self, event, joy2Button, js):
        self.joy2Handlers[event].setdefault(joy2Button, list())
        for handler in self.joy2Handlers[event][joy2Button]:
            handler(js)
    def joy2stickMoved(self, evt):
        pass

    def joy2stickPressed(self, evt, id):

        if id == OIS.MB_Left:
            self.leftDown = True
            self.ms = self.joy2stick.getjoy2StickState()
            print self.ms.X.abs, self.ms.Y.abs
            joy2stickRay = self.camera.getCameraToViewportRay((self.ms.X.abs + 50) / float(evt.get_state().width), (self.ms.Y.abs + 25) / float(evt.get_state().height))
            self.raySceneQuery.setRay(joy2stickRay)
            result = self.raySceneQuery.execute()
            if len(result) > 2:
                    if result[2].movable:
                        print result[2].movable.getName()
                        for ent in self.inputMgr.engine.entityMgr.entList:
                            if (ent.uiname + str(ent.eid)) == result[2].movable.getName():
                                if self.inputMgr.keyboard.isKeyDown(OIS.KC_LSHIFT):
                                    self.inputMgr.engine.selectionMgr.addSelected(ent)
                                else:
                                    self.inputMgr.engine.selectionMgr.selectEnt(ent)
                                

        if id == OIS.MB_Right:
            self.rightDown = True

    def joy2stickReleased(self, evt, id):
        if id == OIS.MB_Left:
            self.leftDown = False
        if id == OIS.MB_Right:
            self.rightDown = False       
        
        
        
        
        

        
        
        
        
        
        
        
        
        


