# Networking manager. Manage networking. Create networking threads, find clients/servers, sync entities

import ogre.renderer.OGRE as ogre
import math

class CameraMgr:
    def __init__(self, engine):
        self.engine = engine
        self.watchingMissile = False
        
    def init(self):
        '''Root and SceneManager'''
        self.root = self.engine.gfxMgr.root
        self.sceneManager = self.engine.gfxMgr.sceneManager


        '''Cameras'''
        self.camera_Main = self.sceneManager.createCamera("camera_Main")
        self.camera_P1 = self.sceneManager.createCamera("Camera_P1")
        self.camera_P2 = self.sceneManager.createCamera("Camera_P2")

        '''ViewPorts and renderWindow'''
        self.renderWindow = self.root.getAutoCreatedWindow()
        self.viewPort_Main = self.renderWindow.addViewport(self.camera_Main, 10, 0, 0, 1, 1)
        self.viewPort_P1 = self.renderWindow.addViewport(self.camera_P1, 1, 0, 0, 0.5, 1)
        self.viewPort_P2 = self.renderWindow.addViewport(self.camera_P2, 2, 0.5, 0, 0.5, 1)


        '''Attach Cameras to Nodes:'''


        '''Main Camera'''
        node_Main_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_Main_1',
                                                                    (1000, 200, 200))
        node_Main_camera.yaw(math.radians(90))
        node1 = node_Main_camera.createChildSceneNode('PitchNode_Main_1')
        node_Main_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_Main_2',
                                                                    (1000, 200, 200))
        node_Main_camera.yaw(math.radians(0))
        node2 = node_Main_camera.createChildSceneNode('PitchNode_Main_2')
        node_Main_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_Main_3',
                                                                    (1000, 200, 200))
        node_Main_camera.yaw(math.radians(150))
        node3 = node_Main_camera.createChildSceneNode('PitchNode_Main_3')
        node_Main_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_Main_4',
                                                                    (1000, 200, 200))
        node_Main_camera.yaw(math.radians(-90))
        node4 = node_Main_camera.createChildSceneNode('PitchNode_Main_4')

        node1.attachObject(self.camera_Main)

        '''Player 1 Camera'''
        node_P1_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P1_1', (-1000, 200, 200))
        node_P1_camera.yaw(math.radians(-90))
        node1 = node_P1_camera.createChildSceneNode('PitchNode_P1_1')
        node_P1_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P1_2',
                                                                   (-1500, 200, 200))
        node_P1_camera.yaw(math.radians(-90))
        node2 = node_P1_camera.createChildSceneNode('PitchNode_P1_2')
        node1.attachObject(self.camera_P1)

        '''Player 2 Camera'''
        node_P2_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P2_1', (-1000, 200, 200))
        node_P2_camera.yaw(math.radians(-90))
        node1 = node_P2_camera.createChildSceneNode('PitchNode_P2_1')
        node_P2_camera = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode_P2_2',
                                                                   (-1500, 200, 200))
        node_P2_camera.yaw(math.radians(-90))
        node2 = node_P2_camera.createChildSceneNode('PitchNode_P2_2')
        node1.attachObject(self.camera_P2)


        '''Camera Vectors'''
        self.camVec_Main = ogre.Vector3(0,0,0)
        self.camVec_P1 = ogre.Vector3(0,0,0)
        self.camVec_P2 = ogre.Vector3(0,0,0)

        '''Camera Nodes'''
        self.camNode_Main = self.camera_Main.parentSceneNode
        self.camNode_P1 = self.camera_P1.parentSceneNode
        self.camNode_P2 = self.camera_P2.parentSceneNode

        '''Other Variables'''
        self.camNum_MainMenu = 0
        self.camNum_MainMenu_All = 4
        self.resetTime = 0
        self.direction = ogre.Vector3(0,0,0)


        self.Player1 = self.engine.entityMgr.entList[0]
        self.Player2 = self.engine.entityMgr.entList[1]
        self.P1_CamPosition = ogre.Vector3(self.Player1.pos.x + (400 * (-math.cos(math.radians(self.Player1.desiredHeading)))), 
                                           self.Player1.pos.y + 50, 
                                           self.Player1.pos.z + (400 * (-math.sin(math.radians(self.Player1.desiredHeading)))))
        self.P2_CamPosition = ogre.Vector3(self.Player2.pos.x + (400 * (-math.cos(math.radians(self.Player2.desiredHeading)))), 
                                           self.Player2.pos.y + 50, 
                                           self.Player2.pos.z + (400 * (-math.sin(math.radians(self.Player2.desiredHeading)))))


    def tick(self, dt):
        if not self.watchingMissile:
            self.P1_CamPosition = ogre.Vector3(self.Player1.pos.x + (400 * (-math.cos(math.radians(self.Player1.desiredHeading)))), 
                                               self.Player1.pos.y + 50, 
                                               self.Player1.pos.z + (400 * (-math.sin(math.radians(self.Player1.desiredHeading)))))
            self.P2_CamPosition = ogre.Vector3(self.Player2.pos.x + (400 * (-math.cos(math.radians(self.Player2.desiredHeading)))), 
                                               self.Player2.pos.y + 50, 
                                               self.Player2.pos.z + (400 * (-math.sin(math.radians(self.Player2.desiredHeading)))))

            self.camNode_P1.setPosition(self.P1_CamPosition)
            self.camNode_P2.setPosition(self.P2_CamPosition)

            self.camNode_Main.translate(self.camNode_Main.orientation * self.camVec_Main * dt)
            self.camNode_P1.translate(self.camNode_P1.orientation * self.camVec_P1 * dt)
            self.camNode_P2.translate(self.camNode_P2.orientation * self.camVec_P2 * dt)

        #print self.camNode_Main.orientation


    def stop(self):
        pass

    def start_MainMenu(self):
        self.time = self.engine.inputMgr.inputListener.timer_MainMenu

        if (self.resetTime - self.time <= 0):
            self.camNum_MainMenu += 1
            if self.camNum_MainMenu > self.camNum_MainMenu_All:
                self.camNum_MainMenu = 1
            self.switchCam_Main()
            self.engine.inputMgr.inputListener.timer_MainMenu = 0

        self.resetTime = 3

    def switchCam_Main(self):

        if self.camNum_MainMenu == 1:
            self.camera_Main.parentSceneNode.detachObject(self.camera_Main)
            self.camNode_Main = self.sceneManager.getSceneNode("CamNode_Main_1")
            self.sceneManager.getSceneNode("PitchNode_Main_1").attachObject(self.camera_Main)
            self.camNode_Main.setPosition(600, 100, 200)
            self.camVec_Main.x = 0
            self.camVec_Main.y = 40
            self.camVec_Main.z = 100
        if self.camNum_MainMenu == 2:
            self.camera_Main.parentSceneNode.detachObject(self.camera_Main)
            self.camNode_Main = self.sceneManager.getSceneNode("CamNode_Main_2")
            self.sceneManager.getSceneNode("PitchNode_Main_2").attachObject(self.camera_Main)
            self.camNode_Main.setPosition(-100, 50, 200)
            self.camVec_Main.x = 50
            self.camVec_Main.y = 0
            self.camVec_Main.z = 0
        if self.camNum_MainMenu == 3:
            self.camera_Main.parentSceneNode.detachObject(self.camera_Main)
            self.camNode_Main = self.sceneManager.getSceneNode("CamNode_Main_3")
            self.sceneManager.getSceneNode("PitchNode_Main_3").attachObject(self.camera_Main)
            self.camNode_Main.setPosition(50, 50, 200)
            self.camVec_Main.x = 0
            self.camVec_Main.y = 0
            self.camVec_Main.z = 100
        if self.camNum_MainMenu == 4:
            self.camera_Main.parentSceneNode.detachObject(self.camera_Main)
            self.camNode_Main = self.sceneManager.getSceneNode("CamNode_Main_4")
            self.sceneManager.getSceneNode("PitchNode_Main_4").attachObject(self.camera_Main)
            self.camNode_Main.setPosition(-300, 50, 200)
            self.camVec_Main.x = 0
            self.camVec_Main.y = 40
            self.camVec_Main.z = 140

    def end_MainMenu(self):
        self.engine.overlayMgr.setOverlay("Game")
        self.renderWindow.removeViewport(10)
        self.camera_P1.parentSceneNode.detachObject(self.camera_P1)
        self.camNode_P1 = self.sceneManager.getSceneNode("CamNode_P1_2")
        self.sceneManager.getSceneNode("PitchNode_P1_2").attachObject(self.camera_P1)
        self.camNode_P1.yaw(-(math.radians(self.Player1.desiredHeading)))
        self.camera_P2.parentSceneNode.detachObject(self.camera_P2)
        self.camNode_P2 = self.sceneManager.getSceneNode("CamNode_P2_2")
        self.sceneManager.getSceneNode("PitchNode_P2_2").attachObject(self.camera_P2)
        self.camNode_P2.yaw(-(math.radians(self.Player2.desiredHeading)))
            
    def P1_CamTurn_Left(self):
        if self.Player1.speed > 0 or self.Player1.speed < -1:
            self.camNode_P1.yaw(math.radians(self.Player1.turningRate))

    def P1_CamTurn_Right(self):
        if self.Player1.speed > 0 or self.Player1.speed < -1:
            self.camNode_P1.yaw(-(math.radians(self.Player1.turningRate)))

    def P2_CamTurn_Left(self):
        if self.Player2.speed > 0 or self.Player2.speed < -1:
            self.camNode_P2.yaw(math.radians(self.Player2.turningRate))

    def P2_CamTurn_Right(self):
        if self.Player2.speed > 0 or self.Player2.speed < -1:
            self.camNode_P2.yaw(-(math.radians(self.Player2.turningRate)))




    
'''
class P1_Cam:
    def __init__(self, cameraMgr):
        self.cameraMgr = cameraMgr

    def init(self):
        self.Player1 = self.inputMgr.engine.entityMgr.entList[0]
        self.P1_CamPosition = ogre.Vector3(self.Player1.pos.x + (400 * (-math.cos(math.radians(self.Player1.desiredHeading )))), 
                                           self.Player1.pos.y + 50, 
                                           self.Player1.pos.z + (400 * (-math.sin(math.radians(self.Player1.desiredHeading )))))

    def tick(self):


class P2_Cam:
    def __init__(self, cameraMgr):
        self.cameraMgr = cameraMgr

    def init(self):
        pass
'''
