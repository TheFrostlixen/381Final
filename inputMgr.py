#Andrew Menard and Brian Gaunt
#CS 381
#Input Manager

"""
    USE TUTORIAL #5
"""
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS


'''






'''


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
        self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
        self.createFrameListener()

    def createFrameListener(self):
        self.exitListener = ExitListener(self)
        self.root.addFrameListener(self.exitListener)
        self.inputListener = InputListener(self)
        self.root.addFrameListener(self.inputListener)
    
    def tick(self, dt):
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
        self.camera1 = self.inputMgr.engine.gfxMgr.camera_P1
        self.camera2 = self.inputMgr.engine.gfxMgr.camera_P2
        self.sceneManager = self.inputMgr.engine.gfxMgr.sceneManager

        self.camNode_P1 = self.camera1.parentSceneNode
        self.camNode_P2 = self.camera2.parentSceneNode
        self.rotate = 0.006
        self.move = 250
        self.moveFast = 1000
        self.BDown = False
        self.direction = ogre.Vector3(0, 0, 0)

        self.toggle_P1 = 0
        self.toggle_P2 = 0

        self.P1_FreeRoam = True
        self.P2_FreeRoam = True


        self.keepRendering = self.inputMgr.keepRendering

    def frameStarted(self, frameEvent):
        self.keyboard.capture()

        #process unbuffered key input for Escape
        self.keyPressed(frameEvent)

        self.Player1 = self.inputMgr.engine.entityMgr.entList[0]
        self.Player2 = self.inputMgr.engine.entityMgr.entList[1]

        self.P1_Node = self.Player1.uiname + 'node' + str(self.Player1.pos)

        self.P1_CamPosition = ogre.Vector3(self.Player1.pos.x - 400, self.Player1.pos.y + 50, self.Player1.pos.z)
        self.P2_CamPosition = ogre.Vector3(self.Player2.pos.x - 400, self.Player2.pos.y + 50, self.Player2.pos.z)

        # Update the toggle timer.
        if self.toggle_P1 >= 0:
            self.toggle_P1 -= frameEvent.timeSinceLastFrame

        if self.toggle_P2 >= 0:
            self.toggle_P2 -= frameEvent.timeSinceLastFrame


        ##############################
        ## PLAYER 1 CAMERA CHANGING ##
        ##############################

        if self.toggle_P1 < 0 and self.keyboard.isKeyDown(OIS.KC_1):
            self.P1_FreeRoam = True
            # Update the toggle timer.
            self.toggle_P1 = 0.1
            # Attach the camera to PitchNode1.
            self.camera1.parentSceneNode.detachObject(self.camera1)
            self.camNode_P1 = self.sceneManager.getSceneNode("CamNode_P1_1")
            self.sceneManager.getSceneNode("PitchNode_P1_1").attachObject(self.camera1)
 
        elif self.toggle_P1 < 0 and self.keyboard.isKeyDown(OIS.KC_2):
            self.P1_FreeRoam = False
            # Update the toggle timer.
            self.toggle_P1 = 0.1
            # Attach the camera to PitchNode2.
            self.camera1.parentSceneNode.detachObject(self.camera1)
            self.camNode_P1 = self.sceneManager.getSceneNode("CamNode_P1_2")
            self.sceneManager.getSceneNode("PitchNode_P1_2").attachObject(self.camera1)

        if not self.P1_FreeRoam:
            self.camNode_P1.setPosition(self.P1_CamPosition)
            #self.camNode_P1.lookAt((self.Player1.uiname + 'node' + str(self.Player1.pos)), self.Player1.pos)
 

        ##############################
        ## PLAYER 2 CAMERA CHANGING ##
        ##############################

        if self.toggle_P2 < 0 and self.keyboard.isKeyDown(OIS.KC_3):
            self.P2_FreeRoam = True
            # Update the toggle timer.
            self.toggle_P2 = 0.1
            # Attach the camera to PitchNode1.
            self.camera2.parentSceneNode.detachObject(self.camera2)
            self.camNode_P2 = self.sceneManager.getSceneNode("CamNode_P2_1")
            self.sceneManager.getSceneNode("PitchNode_P2_1").attachObject(self.camera2)
 
        elif self.toggle_P2 < 0 and self.keyboard.isKeyDown(OIS.KC_4):
            self.P2_FreeRoam = False
            # Update the toggle timer.
            self.toggle_P2 = 0.1
            # Attach the camera to PitchNode2.
            self.camera2.parentSceneNode.detachObject(self.camera2)
            self.camNode_P2 = self.sceneManager.getSceneNode("CamNode_P2_2")
            self.sceneManager.getSceneNode("PitchNode_P2_2").attachObject(self.camera2)

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
            # Yaw Right
            if self.keyboard.isKeyDown(OIS.KC_E):
                self.camNode_P1.yaw(-self.rotate)
            # Pitch Left
            if self.keyboard.isKeyDown(OIS.KC_Z):
                self.camNode_P1.pitch(self.rotate)
            # Pitch Right
            if self.keyboard.isKeyDown(OIS.KC_C):
                self.camNode_P1.pitch(-self.rotate)
            # Roll Left
            if self.keyboard.isKeyDown(OIS.KC_O):
                self.camNode_P1.roll(self.rotate)
            # Roll Right
            if self.keyboard.isKeyDown(OIS.KC_P):
                self.camNode_P1.roll(-self.rotate)
        
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
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        


