import multiprocessing as mp
from world import World
from settings import *
from helpers import *
import math
import copy
import queue
""""
File that contains everything to run a threaded ray marcher and general lighting system

        Main Thread                                               Lighting System
  ┌────────────────────────────┐                           ┌────────────────────────────┐
  │                            │queue of lighting event    │                            │
  │   All world edits trigger  ├─────────────────────────► │                            │
  │   lighting event           │                           │                            │
  │                            │                           │                            │
  │                            │                           │                            │
  │                            │                           │                            │
  │                            │                           │                            │
  │                            │ ◄──────────────────────── │                            │
  │                            │ queue of updated lighting:│                            │
  └────────────────────────────┘ Tile pos and new light    └────────────────────────────┘
                                 level

types of lighting events:
Additive: new light source added
Subtractive: light source removed
Mixed: unrelated tile edit


workload format:








the Lighting System thread maintains mirror of World matrix with only translucency information
Lighting events are used to update this mirror

To avoid filling the queue on game start, the main thread generates,pickles and sends the translucency matrix.
The main thread reads of the queue of returning block update information and handles them at it's leisure. it will not neceserally handle everything in the queue every frame, only ~50






every 

to be clear, i recognize the ridiculousness of running a ray marcher in python on the cpu of a cpu bound game 


"""
EMISSION_LEVEL_TO_INTENSITY_SCALE = 1
EMISSION_LEVEL_RAY_COUNT_SCALE = 40
rays = []

class Ray():
    """
    creates a ray that can be used to calculate volumetrics and lighting
    
    """
    speed = TILE_WIDTH/4
    def __init__(self,originX,originY,angle,intensity,world) -> None:
        #self.color = (Color(r,g,b)/255)*intensity
        
        self.xspeed = math.cos(angle)*self.speed
        self.yspeed = math.sin(angle)*self.speed

        self.x,self.y = self.getPos(originX,originY)

        self.x += TILE_WIDTH/2
        self.y += TILE_HEIGHT/2

        self.origin = (originX,originY)
        self.intensity = intensity
        self.world = world
        self.lastTileX = 0
        self.lastTileY = 0
        self.tile = None


    def step(self):
        tileX,tileY = 0,0
        
    
        
        
        tileX,tileY = self.getBlock(self.x,self.y)
        
        if self.x < 0 or self.x > WORLD_WIDTH*TILE_WIDTH:
            #print("out of bounds x")
            return(0)
        if self.y < 0 or self.y > WORLD_HEIGHT*TILE_HEIGHT:
            #print("out of bounds y")
            return(0)

        
        
        self.tile = self.world[tileX,tileY]
        
        #self.color *= tile.tile.translucency
        # clone = copy.copy(self)
        # clone.color = copy.copy(self.color)

        #self.tile.lighting.passthroughs.append(clone)

        self.lastTileX = tileX
        self.lastTileY = tileY

        while self.lastTileX == tileX and self.lastTileY == tileY:
            #print("repeat")
            #self.color.r = self.color.r*(1-self.tile.tile.colorTranslucency.r)
            #self.color.g = self.color.g*(1-self.tile.tile.colorTranslucency.g)
            #self.color.b = self.color.b*(1-self.tile.tile.colorTranslucency.b)


            self.intensity *= self.tile.translucency
            #print(self.color,tile.tile.colorTranslucency, )
            #self.tile.lighting.lighting.r += self.color.r
            #self.tile.lighting.lighting.g += self.color.g
            #self.tile.lighting.lighting.b += self.color.b
            self.tile.lightLevel += self.intensity
            self.x += self.xspeed
            self.y += self.yspeed
            tileX,tileY = self.getBlock(self.x,self.y)
        
        #buffers.updateTile(self.lastTileX ,self.lastTileY )
        

        
        #print("raying and tracing", self.x,self.y,self.xspeed,self.yspeed,self.intensity)
        return(self.lastTileX ,self.lastTileY, self.tile.lightLevel)




    def getBlock(self,x,y):
        """
        given a global pixel cord, return the square it falls on
        Args:
            x: global pixel cord x
            y: global pixel cord y
        """

        return((int(x/TILE_WIDTH),int(y/TILE_HEIGHT)))



        pass
    def getPos(self,x,y):
        """
        given a tile it returns where it's global pixel cords are
        """

        return((int(x*TILE_WIDTH),int(y*TILE_HEIGHT)))

        pass
    #def reStep(self,count, buffers):

class lightingCell:

    def __init__(self,translucency,lightLevel,emissionlevel) -> None:
        self.translucency = translucency
        self.lightLevel = lightLevel
        self.emissionlevel = emissionlevel
        self.rays = {}
        pass

















def lightingSystemStart(eventsQ: mp.Queue, updatesQ: mp.Queue, lightingMatrix: Matrix):
    global rays
    #updates: x,y,lightLevel
    #events:  x,y,translucency,emissionlevel
    
    for x in range(lightingMatrix.width):
        for y in range(lightingMatrix.height):
            translucency,lightLevel,emissionlevel = lightingMatrix[x,y]
            lightingMatrix[x,y] = lightingCell(translucency,lightLevel,emissionlevel)


            

    while True:
        try:
            event = eventsQ.get_nowait()
            if event:
                x,y,translucency,emissionlevel = event
                cell = lightingMatrix[x,y]
                emissionDelta = emissionlevel-cell.emissionlevel

                if emissionDelta > 0:
                    count = int(EMISSION_LEVEL_RAY_COUNT_SCALE * emissionlevel)
                    for i in range(count):
                        rays.append(  Ray(x,y, (6.283/count) *i,emissionlevel*EMISSION_LEVEL_TO_INTENSITY_SCALE,lightingMatrix)        )
        except queue.Empty:
            pass

        offset = 0
        #print("ru")
        for i in range(len(rays)):
            ray = rays[i - offset]
            x,y,intensity = ray.step()
            if intensity < LIGHTING_CUTOFF:
                #print("killing")
                del rays[i - offset]
                offset += 1
            
            updatesQ.put((x,y,intensity))

            




        pass



    pass






class LightingInterface():
    """
    used to create and communicate with the lighting system thread
    
    """
    def __init__(self,world) -> None:
        


        self.events = mp.Queue() #outgoing 

        self.updates = mp.Queue() #incoming
        self.lightingMatrix = Matrix(world.width,world.height)
        self.world = world
        self.initLighting()
        
        self.lightingSystem = mp.Process(target=lightingSystemStart, args=(self.events,self.updates,self.lightingMatrix))
        self.lightingSystem.daemon = True
        self.lightingSystem.start()
        #del self.lightingMatrix




        pass
    

    def initLighting(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                cell = self.world[x,y]
                translucency = cell.tile.translucency
                emissionlevel = cell.tile.emissionlevel
                lightLevel = cell.lighting.lighting

                self.lightingMatrix[x,y] = (translucency,lightLevel,emissionlevel)
    


    def sendEvent(self,x,y):
        cell = self.world[x,y]
        translucency = cell.tile.translucency
        emissionlevel = cell.tile.emissionlevel
        #lightLevel = cell.lighting.lighting
        self.events.put((x,y,translucency,emissionlevel))
    

    def UpdateFromQueue(self,buffers):
        try:
            data = self.updates.get_nowait()
            if data:
                
                x,y,lightLevel = data
                #print("data",x,y,lightLevel)
                self.world[x,y].lighting.lighting = lightLevel
                buffers.updateTile(x,y)
        except queue.Empty:
            pass









