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
        self.collisionRange = 100

class Carrier(Entity):
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
        self.mesh = "carrier.mesh"
        self.uiname = "Carrier"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5


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
        self.acceleration = 0.4
        self.maxSpeed = 100
        self.turningRate = 0.5
        self.mesh = "sleek.mesh"
        self.uiname = "Sleek"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 100

        
class SailBoat(Entity):
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
        self.acceleration = 0.2
        self.maxSpeed = 26
        self.turningRate = 0.5
        self.mesh = "sailboat.mesh"
        self.uiname = "Sail Boat"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5

        
class Missile(Entity):
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
        self.acceleration = 0.3
        self.maxSpeed = 46
        self.turningRate = 0.5
        self.mesh = "missile.mesh"
        self.uiname = "Missile"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5


class CigaretteBoat(Entity):
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
        self.acceleration = 0.4
        self.maxSpeed = 56
        self.turningRate = 0.5
        self.mesh = "cigarette.mesh"
        self.uiname = "Cigarette Boat"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5

        
class Boat(Entity):
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
        self.acceleration = 0.3
        self.maxSpeed = 40
        self.turningRate = 0.5
        self.mesh = "boat.mesh"
        self.uiname = "Boat"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5

        
class JetSki(Entity):
    def __init__(self, engine, id, pos = Vector3(0, 5, 0)):
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
        self.pos = pos + Vector3(0,5,0)
        self.acceleration = 0.3
        self.maxSpeed = 36
        self.turningRate = 0.5
        self.mesh = "jetski.mesh"
        self.uiname = "Jet Ski"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5

        
class Yacht(Entity):
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
        self.acceleration = 0.4
        self.maxSpeed = 46
        self.turningRate = 0.5
        self.mesh = "yacht.mesh"
        self.uiname = "Yacht"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5

        
class SpeedBoat(Entity):
    def __init__(self, engine, id, pos = Vector3(0, 5, 0)):
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
        self.pos = pos + Vector3(0,5,0)
        self.acceleration = 1.0
        self.maxSpeed = 100
        self.turningRate = 1.0
        self.mesh = "speedboat.mesh"
        self.uiname = "Speed Boat"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 5

        
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
        self.acceleration = 0.2
        self.maxSpeed = 50
        self.turningRate = 0.5
        self.mesh = "destroyer.mesh"
        self.uiname = "Destroyer"
        self.isSelected = False
        self.engine = engine
        self.sound = "windsobey.ogg"
        self.collisionRange = 100





















