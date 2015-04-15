#Andrew Menard and Brian Gaunt
#CS 381
#Graphics Manager

"""
    USE TUTORIAL #6
"""

import ogre.renderer.OGRE as ogre

class GfxMgr:
    
    def __init__(self, engine):
        self.engine = engine
    
    def init(self):
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()

    def createRoot(self):
        self.root = ogre.Root()

    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")

        #start looping through the parsed config file
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            #aquire the section to get all contents out
            secName = seci.peekNextKey() #section name (which is the group of the resources)
            settings = seci.getNext()
            #
            for item in settings:
                typeName = item.key #type of resource (zip, folder, etc)
                archName = item.value #filename of the resource itself
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
                #add all three things to the ResourceGroupManager

    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog! -> Application.setupRenderSystem()")

    def createRenderWindow(self):
        self.root.initialise(True, "Render Window - Brian Gaunt")

    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

    def setupScene(self):
        
        '''SETUP SCENEMANAGER'''
        self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")
        self.sceneManager.setAmbientLight(ogre.ColourValue(1, 1, 1))
        
        '''SETUP ENVIRONMENT'''
        plane = ogre.Plane ((0, 1, 0), 0)
        meshManager = ogre.MeshManager.getSingleton ()
        meshManager.createPlane ('Ground', 'General', plane,
                                     10000, 10000, 20, 20, True, 
                                     1, 5, 5, (0, 0, 1))
        ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode ().attachObject (ent)
        ent.setMaterialName ('OceanCg')
        ent.castShadows = False
        self.sceneManager.setSkyBox (True, "Examples/MorningSkyBox", 5000, False)
        #sceneManager.setSkyDome (True, "Examples/CloudySky", 5, 8)

        '''SETUP CAMERA AND VIEWPORT'''
        self.camera = self.sceneManager.createCamera("Camera1")
        viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
        node = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode1',
                                                               (0, 200, 1000))
        node = node.createChildSceneNode('PitchNode1')
        node.attachObject(self.camera)


    def tick(self, dt):
        self.engine.keepRunning = self.root.renderOneFrame(dt) #boolean type must return
    
    def stop(self):
        pass
