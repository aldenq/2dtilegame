import physics
from helpers import *
import time,pickle
class EntityManager():

    def __init__(self,world) -> None:
        self.entities = []
        self.world = world
    
    def __getitem__(self,loc):
        return(self.entities[loc])
    
    def __setitem__(self,loc,value):
        x,y = loc
        self.entities[loc] = value
    
    def spawn(self,entity):
        entity.world = self.world
        self.entities.append(entity)
        return(len(self.entities)-1)

    def spawnClone(self,entity):
        pass


    def deleteEntity(self):
        pass
    
    def simulateEntities(self):
        for entity in self.entities:
            entity.simulate()
        pass

    def drawEntities(self,surface,camera):
        for entity in self.entities:
            entity.drawEnt(surface,camera)
    
    def getCollisions(self,collider):
        overlaps = []
        for entity in self.entities:
            if entity.collider.checkOverlap(collider):
                overlaps.append(entity)
        return(overlaps)









class Entity():
    def __init__(self,x,y,xspeed,yspeed,width,height, lifeSpan = 0) -> None:

        self.xspeed = xspeed
        self.yspeed = yspeed
        self.x = x
        self.y = y
        self.world = None
        self.width = width
        self.height = height
        self.id = None
        self.collider = physics.Collider(x,y,self.width,self.height)

        self.cullOffScreen= False
        self.simulateOffscreen = True
        self.lifeSpan = lifeSpan #how long the entity should exist, if 0 then indefinite
        self.age = 0
        self.dead = False
        self.spawnTime = time.time()
        self.visible = True



        self.AI = None
        self.draw = None

    def simulate(self):
        if callable(self.AI):
            self.AI(self)
        

        self.collider.x = self.x
        self.collider.y = self.y
        #print(self.xspeed,self.yspeed)
        self.collider.xSpeed = self.xspeed
        self.collider.ySpeed = self.yspeed
        #print(self.yspeed)
        #print(self.xspeed)
        self.collider.runPhysics(self.world)

        self.x = self.collider.x
        self.y = self.collider.y

        self.yspeed = self.collider.ySpeed
        self.xspeed = self.collider.xSpeed
        
        pass
    
    def drawEnt(self,surface,camera):
        if self.visible:
            if callable(self.draw):
                self.draw(self,surface,camera)
            else:
                self.collider.draw(surface,camera)


    



    








        pass