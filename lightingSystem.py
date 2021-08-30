import multiprocessing as mp
from typing import NewType
from world import World
from settings import *
from helpers import *
import math
import copy
import queue
import random
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



most optimizations in this thread should be done with the intent of speeding up the main thread.
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
        #print(self.x)
    
        
        
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
        preLevel = self.tile.lightLevel
        preIntensity = self.intensity
        preX = self.x
        preY = self.y

        newLevel = preLevel

        while self.lastTileX == tileX and self.lastTileY == tileY:

            #print("repeat")
            #self.color.r = self.color.r*(1-self.tile.tile.colorTranslucency.r)
            #self.color.g = self.color.g*(1-self.tile.tile.colorTranslucency.g)
            #self.color.b = self.color.b*(1-self.tile.tile.colorTranslucency.b)
            #print("repeating",self.xspeed,self.yspeed)

            self.intensity *= self.tile.translucency
            #print(self.color,tile.tile.colorTranslucency, )
            #self.tile.lighting.lighting.r += self.color.r
            #self.tile.lighting.lighting.g += self.color.g
            #self.tile.lighting.lighting.b += self.color.b

            newLevel += self.intensity


            
            
            self.x += self.xspeed
            self.y += self.yspeed
            tileX,tileY = self.getBlock(self.x,self.y)
        
        #buffers.updateTile(self.lastTileX ,self.lastTileY )
        

        
        #print("raying and tracing", self.x,self.y,self.xspeed,self.yspeed,self.intensity)
       
        levelDelta = newLevel-preLevel #the summed effect of all rays from the same origin to this tile

        speedloc = (self.xspeed,self.yspeed,preX,preY,self.origin)

        # if speed == (0,0):
        #     print("bad speed")
        #print(speed,"speed")
        #print(self.tile.rays)
        if speedloc in self.tile.rays: 
            lastRay = self.tile.rays[speedloc]
            rayDelta = levelDelta-lastRay[0]
            
            self.tile.rays[speedloc] = [levelDelta,  preIntensity]




        else:  #first time from specified origin 
            rayDelta = levelDelta
            #print(speed)
            self.tile.rays[speedloc] = [levelDelta,preIntensity]  #pre intensity is stored rather than the actual intensity so that the step can be re simulated later


        self.tile.lightLevel += rayDelta
        #self.tile.rays[self.origin] 


        return(self.lastTileX ,self.lastTileY, self.tile.lightLevel,self.intensity,rayDelta)




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

                if emissionDelta > 0: #if emissive event (new light source being added)
                    count = int(EMISSION_LEVEL_RAY_COUNT_SCALE * emissionlevel)
                    for i in range(count):
                        rays.append(  Ray(x,y, (6.283/count) *i,emissionlevel*EMISSION_LEVEL_TO_INTENSITY_SCALE,lightingMatrix))
                
                
                
                if emissionDelta == 0: #if standard block is added or deleted
                    

                    translucencyDelta = translucency-lightingMatrix[x,y].translucency


                    #print(translucencyDelta, "tdelta")
                    lightingMatrix[x,y].translucency = translucency
                    for speedloc in cell.rays:
                        levelDelta,intensity = cell.rays[speedloc]
                        #intensityDelta = translucencyDelta*intensity


                        #print(intensityDelta, "int delta")
                        
                        ray= Ray(0,0, 0,intensity,lightingMatrix)
                        ray.xspeed,ray.yspeed,x,y,origin = speedloc
                        #print(ray.xspeed,ray.yspeed,"new")
                        ray.x = x
                        ray.y = y
                        ray.origin = origin
                        rays.append(ray)




                        #print(cell.rays[origin] , "value")




                    pass


                else: #if emiter is getting destroyed
                    pass
        except queue.Empty:
            pass

        offset = 0
        #print("ru")
        lastX = None
        lastY = None
        lastLL = 0
        for i in range(len(rays)):
            ray = rays[i - offset]
            x,y,lightLevel,intensity,delta = ray.step()
            #updatesQ.put((x,y,lightLevel))

            if lastX== x and lastY==y: #rays that are near each other in the rays list have a higher probability of being near each other in space
                lastLL = lightLevel
            else:
                if lastX != None:
                    updatesQ.put((lastX,lastY,lastLL))
                lastLL = lightLevel
                lastX = x
                lastY = y

                


            #print(x,y,lightLevel,intensity,delta)
            if abs(delta) < LIGHTING_CUTOFF and abs(intensity) < LIGHTING_CUTOFF:
                #print("killing")
                del rays[i - offset]
                offset += 1

        if lastX != None:
            updatesQ.put((lastX,lastY,lastLL))
        
            

            




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

                tile = cell.tile
                if not tile:
                    tile = cell.backgroundTile
                translucency = tile.translucency
                emissionlevel = tile.emissionlevel
                lightLevel = cell.lighting.lighting

                self.lightingMatrix[x,y] = (translucency,lightLevel,emissionlevel)
    


    def sendEvent(self,x,y):
        cell = self.world[x,y]
        tile = cell.tile
        if not tile:
            tile = cell.backgroundTile

        translucency = tile.translucency
        emissionlevel = tile.emissionlevel
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
                return(1)
        except queue.Empty:
            return(0)
            pass









