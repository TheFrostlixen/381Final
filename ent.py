#Andrew Menard and Brian Gaunt
from vector import Vector3
from physics import Physics
from renderer import Renderer
from collision import Collision

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
        self.collisionRange = 20


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





















