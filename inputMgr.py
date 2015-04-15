#Andrew Menard and Brian Gaunt
#CS 381
#Input Manager

"""
    USE TUTORIAL #5
"""
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

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
        self.camera = self.inputMgr.engine.gfxMgr.camera1
        self.sceneManager = self.inputMgr.engine.gfxMgr.sceneManager

        self.camNode = self.camera.parentSceneNode.parentSceneNode
        self.rotate = 0.006
        self.move = 250
        self.moveFast = 1000
        self.BDown = False
        self.direction = ogre.Vector3(0, 0, 0)

        self.keepRendering = self.inputMgr.keepRendering

    def frameStarted(self, frameEvent):
        self.keyboard.capture()

        #process unbuffered key input for Escape
        self.keyPressed(frameEvent)

        #translate the camera based on time
        self.camNode.translate(self.camNode.orientation
            * self.direction
            * frameEvent.timeSinceLastFrame)

        #check for Key release to stop moving the camera.
        self.keyReleased(frameEvent)

        return True

    def keyPressed(self, frameEvent):
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
            self.camNode.yaw(self.rotate)
        # Yaw Right
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.camNode.yaw(-self.rotate)
        # Pitch Left
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.camNode.pitch(self.rotate)
        # Pitch Right
        if self.keyboard.isKeyDown(OIS.KC_C):
            self.camNode.pitch(-self.rotate)
        # Roll Left
        if self.keyboard.isKeyDown(OIS.KC_O):
            self.camNode.roll(self.rotate)
        # Roll Right
        if self.keyboard.isKeyDown(OIS.KC_P):
            self.camNode.roll(-self.rotate)
        
        return True

    def keyReleased(self, frameEvent):
        # Undo change to the direction vector when the key is released to stop movement.
        # Move Forward.
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
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        


