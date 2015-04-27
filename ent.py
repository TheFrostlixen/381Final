#Andrew Menard and Brian Gaunt
from vector import Vector3
from physics import Physics
from renderer import Renderer
from collision import Collision



"""
MESHES:

WoodPallet.mesh - very small, possibly used to slow down boats?
tudorhouse.mesh - very very large cottage house
RZR-002.mesh - very small jet plane
razor.mesh - very large jet plane
ogrehead.mesh - use for speed boosts?
knot.mesh - large knot with no texture; could be used for decorative obstacle?
jaiqua.mesh - small woman in blue jumpsuit in wierd pose
geosphere8000.mesh - very very large sphere with no texture
geosphere4500.mesh - same
fish.mesh - small fish; use for blue shell?
facial.mesh - some large caveman lookin brown dude's head with shades on
column.mesh - just a column with no texture; should use for track boundaries
Barrel.mesh - very very small brown barrel
athene.mesh - large athena statue with no texture
alienship.mesh - very small alienship with no texture, use for boat options?

"""

class Entity:

    
    def __init__(self, engine, id, pos = Vector3(0,0,0), mesh = 'robot.mesh', vel = Vector3(0, 0, 0), acceleration = 0, turningRate = 0, maxSpeed = 0, yaw = 0):
        
        self.engine = engine
        self.vel = vel
        self.aspects = []
        self.aspectTypes = [Physics, Renderer, Collision]
        self.speed = 0
        self.heading = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.collisionRange = 1000
        self.yaw = yaw
        self.isSelected = False

        self.mesh = mesh
        self.id = id
        self.pos = pos        
        self.maxSpeed = maxSpeed
        self.acceleration = acceleration
        self.turningRate = turningRate
        
    def init(self):
        self.initAspects()

    def initAspects(self):
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self))

    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)        

    def __str__(self):
        x = "Entity: %s \nPos: %s, Vel: %s, yaw: %f" % (self.id, str(self.pos), str(self.vel), self.yaw)
        return x

#-----------------------------------------------------------------------------------
# ENTITY TYPES
#-----------------------------------------------------------------------------------
class Obstacle(Entity):
    def __init__(self, engine, id, pos = Vector3(0, 0, 0)):
        self.currentYaw = 0
        self.vel = Vector3(0,0,0)
        self.aspects = []
        self.aspectTypes = [Physics, Renderer, Collision]
        self.speed = 0
        self.heading = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.yaw = 0
        self.eid = id
        self.pos = pos
        self.acceleration = 0.1
        self.maxSpeed = 100
        self.turningRate = 0.5
        self.mesh = "cube.mesh"
        self.uiname = "Obstacle"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 60

class Item_Boost(Entity):
    def __init__(self, engine, id, pos = Vector3(0, 0, 0)):
        self.currentYaw = 0
        self.vel = Vector3(0,0,0)
        self.aspects = []
        self.aspectTypes = [Physics, Renderer, Collision]
        self.speed = 0
        self.heading = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.yaw = 0
        self.eid = id
        self.pos = pos
        self.acceleration = 0.1
        self.maxSpeed = 100
        self.turningRate = 0.5
        self.mesh = "ogrehead.mesh"
        self.uiname = "Item_Boost"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 30


class Sleek(Entity):
    def __init__(self, engine, id, pos = Vector3(0, 0, 0)):
        self.currentYaw = 0
        self.vel = Vector3(0,0,0)
        self.aspects = []
        self.aspectTypes = [Physics, Renderer, Collision]
        self.speed = 0
        self.heading = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.yaw = 0    
        self.eid = id
        self.pos = pos
        self.acceleration = 2.0
        self.maxSpeed = 1000
        self.turningRate = 1.0
        self.mesh = "sleek.mesh"
        self.uiname = "Sleek"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 30
        self.boosting = False

        
class Destroyer(Entity):
    def __init__(self, engine, id, pos = Vector3(0, 0, 0)):
        self.currentYaw = 0
        self.vel = Vector3(0,0,0)
        self.aspects = []
        self.aspectTypes = [Physics, Renderer, Collision]
        self.speed = 0
        self.heading = 0
        self.desiredSpeed = 0
        self.desiredHeading = 0
        self.yaw = 0    
        self.eid = id
        self.pos = pos
        self.acceleration = 2.0
        self.maxSpeed = 1200
        self.turningRate = 1.0
        self.mesh = "destroyer.mesh"
        self.uiname = "Destroyer"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 30
        self.boosting = False




















