#Andrew Menard and Brian Gaunt
#CS 381
#Input Manager

"""
    USE TUTORIAL #5
"""
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math

class JoyEvent:
    BUTTON_PRESSED  = 0
    BUTTON_RELEASED = 1
    AXIS_MOVED      = 2
    POV_MOVED       = 3
    VECTOR3_MOVED   = 4
    NUM             = 5
    INVALID         = 6

class JoyButtons: # XBox Controller, the buttons need to be checked
    BACK       = 0
    A          = 1
    B          = 2
    X          = 3
    Y          = 4
    LEFT       = 5
    RIGHT      = 6
    START      = 7
    XBOX       = 8
    LEFT_AXIS  = 9
    RIGHT_AXIS = 10
    POV        = 11

    NUM     = 12
    LIST    = [BACK, A, B, X, Y, LEFT, RIGHT, START, XBOX, LEFT_AXIS, RIGHT_AXIS, POV]

class JoyAxes: # XBox Controller
    LEFT_LEFTRIGHT    = 0
    LEFT_UPDOWN       = 1
    LEFT_LEFT         = 2
    RIGHT_LEFTRIGHT   = 3
    RIGHT_UPDOWN      = 4
    RIGHT_RIGHT       = 5
    NUM               = 6

    LIST    = [LEFT_LEFTRIGHT, LEFT_UPDOWN, LEFT_LEFT, RIGHT_LEFTRIGHT, RIGHT_UPDOWN, RIGHT_RIGHT]

class InputMgr():

    def __init__(self, engine):
        self.engine = engine
    
    def init(self):

        self.root = self.engine.gfxMgr.root
        self.keepRendering = True

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
        try:
            self.joystick = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, True)
            print "----------------------------------->Made joystick object"
        except Exception, e:
            self.joystick = None
            print "----------------------------------->No Joy, Don't Worry Be Happy"
            print "----------------------------------->Who uses joysticks anyways? - so 1995"
        if self.joystick:
            self.jMgr = JoyStickListener(self)

        try:
            self.joy2stick = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, True)
            print "----------------------------------->Made joystick object"
        except Exception, e:
            self.joy2stick = None
            print "----------------------------------->No Joy, Don't Worry Be Happy"
            print "----------------------------------->Who uses joysticks anyways? - so 1995"
        if self.joy2stick:
            self.jMgr2 = Joy2StickListener(self)

        self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
        self.jMgr2 = Joy2StickListener(self)
        self.jMgr = JoyStickListener(self)
        self.createFrameListener()

    def createFrameListener(self):
        self.exitListener = ExitListener(self)
        self.root.addFrameListener(self.exitListener)
        self.inputListener = InputListener(self)
        self.root.addFrameListener(self.inputListener)
    
    def tick(self, dt):
        if self.joystick:
            self.joystick.capture()
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
        self.cameraMain = self.cameraMgr.camera_Main
        self.camera1 = self.cameraMgr.camera_P1
        self.camera2 = self.cameraMgr.camera_P2
        self.joystick = self.inputMgr.joystick
        self.joyHandlers = [dict() for x in range(JoyEvent.NUM)]
        self.sceneManager = self.inputMgr.engine.gfxMgr.sceneManager

        self.camNode_Main = self.cameraMain.parentSceneNode
        self.camNode_P1 = self.camera1.parentSceneNode
        self.camNode_P2 = self.camera2.parentSceneNode
        self.rotate = 0.006
        self.move = 250
        self.moveFast = 1000
        self.BDown = False
        self.direction = ogre.Vector3(0, 0, 0)
        self.mainPos = self.camNode_Main.getPosition()

        self.toggle_P1 = 0
        self.toggle_P2 = 0
        self.toggle = 0

        self.timer_MainMenu = 0
        self.timer_Race = 0

        self.mc1 = True
        self.mc2 = False
        self.mc3 = False

        self.mainMenu = True
        self.P1_FreeRoam = True
        self.P2_FreeRoam = True

        self.trigger = True
        self.camNum = 1

        self.keepRendering = self.inputMgr.keepRendering

    def frameStarted(self, frameEvent):
        self.keyboard.capture()

        #process unbuffered key input for Escape
        self.keyPressed(frameEvent)

        self.Player1 = self.inputMgr.engine.entityMgr.entList[0]
        self.Player2 = self.inputMgr.engine.entityMgr.entList[1]

        self.timer_MainMenu += frameEvent.timeSinceLastFrame

        self.P1_CamPosition = ogre.Vector3(self.Player1.pos.x + (400 * (-math.cos(math.radians(self.Player1.desiredHeading )))), 
                                           self.Player1.pos.y + 50, 
                                           self.Player1.pos.z + (400 * (-math.sin(math.radians(self.Player1.desiredHeading )))))
        self.P2_CamPosition = ogre.Vector3(self.Player2.pos.x + (400 * (-math.cos(math.radians(self.Player2.desiredHeading )))), 
                                           self.Player2.pos.y + 50, 
                                           self.Player2.pos.z + (400 * (-math.sin(math.radians(self.Player2.desiredHeading )))))

        # Update the toggle timer.
        if self.toggle_P1 >= 0:
            self.toggle_P1 -= frameEvent.timeSinceLastFrame

        if self.toggle_P2 >= 0:
            self.toggle_P2 -= frameEvent.timeSinceLastFrame

        if self.toggle >= 0:
            self.toggle -= frameEvent.timeSinceLastFrame


        if self.mainMenu and self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_RETURN):
            self.toggle = 0.1
            self.mainMenu = False
            self.cameraMgr.renderWindow.removeViewport(10)
            self.P1_FreeRoam = False
            self.camera1.parentSceneNode.detachObject(self.camera1)
            self.camNode_P1 = self.sceneManager.getSceneNode("CamNode_P1_2")
            self.sceneManager.getSceneNode("PitchNode_P1_2").attachObject(self.camera1)
            self.camNode_P1.yaw(-(math.radians(self.Player1.desiredHeading)))
            self.P2_FreeRoam = False
            self.camera2.parentSceneNode.detachObject(self.camera2)
            self.camNode_P2 = self.sceneManager.getSceneNode("CamNode_P2_2")
            self.sceneManager.getSceneNode("PitchNode_P2_2").attachObject(self.camera2)
            self.camNode_P2.yaw(-(math.radians(self.Player2.desiredHeading)))

        #print self.timer_MainMenu
        
        if self.mainMenu:
            self.cameraMgr.start_MainMenu()



        ##############################
        ## PLAYER 1 CAMERA CHANGING ##
        ##############################

        if self.toggle_P1 < 0 and self.keyboard.isKeyDown(OIS.KC_1) and not self.P1_FreeRoam:
            self.P1_FreeRoam = True
            # Update the toggle timer.
            self.toggle_P1 = 0.1
            # Attach the camera to PitchNode1.
            self.camNode_P1.yaw(math.radians(self.Player1.desiredHeading))
            self.camera1.parentSceneNode.detachObject(self.camera1)
            self.camNode_P1 = self.sceneManager.getSceneNode("CamNode_P1_1")
            self.sceneManager.getSceneNode("PitchNode_P1_1").attachObject(self.camera1)

 
        elif self.toggle_P1 < 0 and self.keyboard.isKeyDown(OIS.KC_2) and self.P1_FreeRoam:
            self.P1_FreeRoam = False
            # Update the toggle timer.
            self.toggle_P1 = 0.1
            # Attach the camera to PitchNode2.
            self.camera1.parentSceneNode.detachObject(self.camera1)
            self.camNode_P1 = self.sceneManager.getSceneNode("CamNode_P1_2")
            self.sceneManager.getSceneNode("PitchNode_P1_2").attachObject(self.camera1)
            self.camNode_P1.yaw(-(math.radians(self.Player1.desiredHeading)))

        if not self.P1_FreeRoam:
            self.camNode_P1.setPosition(self.P1_CamPosition)   
 

        ##############################
        ## PLAYER 2 CAMERA CHANGING ##
        ##############################

        if self.toggle_P2 < 0 and self.keyboard.isKeyDown(OIS.KC_3) and not self.P2_FreeRoam:
            self.P2_FreeRoam = True
            # Update the toggle timer.
            self.toggle_P2 = 0.1
            # Attach the camera to PitchNode1.
            self.camNode_P2.yaw(math.radians(self.Player2.desiredHeading))
            self.camera2.parentSceneNode.detachObject(self.camera2)
            self.camNode_P2 = self.sceneManager.getSceneNode("CamNode_P2_1")
            self.sceneManager.getSceneNode("PitchNode_P2_1").attachObject(self.camera2)
 
        elif self.toggle_P2 < 0 and self.keyboard.isKeyDown(OIS.KC_4) and self.P2_FreeRoam:
            self.P2_FreeRoam = False
            # Update the toggle timer.
            self.toggle_P2 = 0.1
            # Attach the camera to PitchNode2.
            self.camera2.parentSceneNode.detachObject(self.camera2)
            self.camNode_P2 = self.sceneManager.getSceneNode("CamNode_P2_2")
            self.sceneManager.getSceneNode("PitchNode_P2_2").attachObject(self.camera2)
            self.camNode_P2.yaw(-(math.radians(self.Player2.desiredHeading)))

        if not self.P2_FreeRoam:
            self.camNode_P2.setPosition(self.P2_CamPosition)

 

        #translate the camera based on time

        self.camNode_P1.translate(self.camNode_P1.orientation
            * self.direction
            * frameEvent.timeSinceLastFrame)

        self.camNode_P2.translate(self.camNode_P2.orientation
            * self.direction
            * frameEvent.timeSinceLastFrame)


        #check for Key release to stop moving the camera.
        self.keyReleased(frameEvent)

        return True


    def keyPressed(self, frameEvent):
        if self.P1_FreeRoam and self.P2_FreeRoam:
            # Accelerate Camera
            if self.keyboard.isKeyDown(OIS.KC_B):
                self.BDown = True
                self.rotate = 0.03
            if not self.keyboard.isKeyDown(OIS.KC_B):
                self.BDown = False
                self.rotate = 0.006
            # Move Forward.
            if self.keyboard.isKeyDown(OIS.KC_W):
                if self.BDown == True:
                    self.direction.z -= self.moveFast
                else:
                    self.direction.z -= self.move
            # Move Backward.
            if self.keyboard.isKeyDown(OIS.KC_S):
                if self.BDown == True:
                    self.direction.z += self.moveFast
                else:
                    self.direction.z += self.move
            # Strafe Left.
            if self.keyboard.isKeyDown(OIS.KC_A):
                if self.BDown == True:
                    self.direction.x -= self.moveFast
                else:
                    self.direction.x -= self.move
            # Strafe Right.
            if self.keyboard.isKeyDown(OIS.KC_D):
                if self.BDown == True:
                    self.direction.x += self.moveFast
                else:
                    self.direction.x += self.move
            # Move Up.
            if self.keyboard.isKeyDown(OIS.KC_PGUP):
                if self.BDown == True:
                    self.direction.y += self.moveFast
                else:
                    self.direction.y += self.move
            # Move Down.
            if self.keyboard.isKeyDown(OIS.KC_PGDOWN):
                if self.BDown == True:
                    self.direction.y -= self.moveFast
                else:
                    self.direction.y -= self.move
            # Yaw Left
            if self.keyboard.isKeyDown(OIS.KC_Q):
                self.camNode_P1.yaw(self.rotate)
                self.camNode_P2.yaw(self.rotate)
            # Yaw Right
            if self.keyboard.isKeyDown(OIS.KC_E):
                self.camNode_P1.yaw(-self.rotate)
                self.camNode_P2.yaw(-self.rotate)
            # Pitch Left
            if self.keyboard.isKeyDown(OIS.KC_Z):
                self.camNode_P1.pitch(self.rotate)
                self.camNode_P2.pitch(self.rotate)
            # Pitch Right
            if self.keyboard.isKeyDown(OIS.KC_C):
                self.camNode_P1.pitch(-self.rotate)
                self.camNode_P2.pitch(-self.rotate)
            # Roll Left
            if self.keyboard.isKeyDown(OIS.KC_O):
                self.camNode_P1.roll(self.rotate)
                self.camNode_P2.roll(self.rotate)
            # Roll Right
            if self.keyboard.isKeyDown(OIS.KC_P):
                self.camNode_P1.roll(-self.rotate)
                self.camNode_P2.roll(-self.rotate)


        if not self.P1_FreeRoam:
            if self.keyboard.isKeyDown(OIS.KC_LEFT):
                if self.Player1.speed > 0 or self.Player1.speed < -1:
                    self.camNode_P1.yaw(math.radians(self.Player1.turningRate))
                    
            if self.keyboard.isKeyDown(OIS.KC_RIGHT):
                if self.Player1.speed > 0 or self.Player1.speed < -1:
                    self.camNode_P1.yaw(-math.radians(self.Player1.turningRate))

        if not self.P2_FreeRoam:
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD4) or self.inputMgr.jMgr.joyLDown:
                if self.Player2.speed > 0 or self.Player2.speed < -1:
                    self.camNode_P2.yaw(math.radians(self.Player2.turningRate))
                    
            if self.keyboard.isKeyDown(OIS.KC_NUMPAD6) or self.inputMgr.jMgr.joyRDown:
                if self.Player2.speed > 0 or self.Player2.speed < -1:
                    self.camNode_P2.yaw(-math.radians(self.Player2.turningRate))
        
        return True

    def keyReleased(self, frameEvent):
        # Undo change to the direction vector when the key is released to stop movement.
        # Move Forward.
        if self.P1_FreeRoam and self.P2_FreeRoam:
            if self.keyboard.isKeyDown(OIS.KC_W):
                if self.BDown == True:
                    self.direction.z += self.moveFast
                else:
                    self.direction.z += self.move
            # Move Backward.
            if self.keyboard.isKeyDown(OIS.KC_S):
                if self.BDown == True:
                    self.direction.z -= self.moveFast
                else:
                    self.direction.z -= self.move
            # Strafe Left.
            if self.keyboard.isKeyDown(OIS.KC_A):
                if self.BDown == True:
                    self.direction.x += self.moveFast
                else:
                    self.direction.x += self.move
            # Strafe Right.
            if self.keyboard.isKeyDown(OIS.KC_D):
                if self.BDown == True:
                    self.direction.x -= self.moveFast
                else:
                    self.direction.x -= self.move
            # Move Up.
            if self.keyboard.isKeyDown(OIS.KC_PGUP):
                if self.BDown == True:
                    self.direction.y -= self.moveFast
                else:
                    self.direction.y -= self.move
            # Move Down.
            if self.keyboard.isKeyDown(OIS.KC_PGDOWN):
                if self.BDown == True:
                    self.direction.y += self.moveFast
                else:
                    self.direction.y += self.move


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
        
        
        
        
        

        
        
        
        
        
        
        
        
        


