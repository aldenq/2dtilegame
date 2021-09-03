
import random
from helpers import *
from settings import *
import noise
import tiles
import math
import copy
class lightingData():
    """
    
    one of the elements that composes a Cell. Stores information about how that cell is lit. 
    Does not change when a tile is updated
    """
    def __init__(self) -> None:
        self.lighting = 0
        self.sunlight = 0
        self.passthroughs = []
        pass


class Cell():
    """
    used to store all information relating to tiles
    
    """
    def __init__(self) -> None:
        self.lighting = lightingData()
        self.tile = None
        self.backgroundTile = None
        pass

    


    
class lightingWorkloadSunlight():

    def __init__(self,x,y,world):
        

        self.x = x
        self.y = y
        # if world[x,y].tile:
        #     if world[x,y].tile.sunlightEmissive > 0: #sunlight emitter
        #         self.y += 1 #if it's a now emitter than no need to re-compute itself, only subsequent 
        # else:
        #     if world[x,y].backgroundTile.sunlightEmissive > 0: #sunlight emitter
        #         self.y += 1 #if it's a now emitter than no need to re-compute itself, only subsequent 

        self.level = world[x,y].lighting.sunlight
        self.radius = 0
        self.world = world
        #self.rays = []
    

    def step(self,buffers):
        for i in range(8):
           
                
            tile = self.world[self.x,self.y].tile
            if not tile:
                tile = self.world[self.x,self.y].backgroundTile

            prevLevel = self.world[self.x,self.y].lighting.sunlight

            self.level = self.world[self.x,self.y - 1].lighting.sunlight * tile.translucency  + tile.sunlightEmissive
            self.world[self.x,self.y].lighting.sunlight = self.level

            buffers.updateTile(self.x ,self.y)
            self.y +=1 

            delta = self.level-prevLevel
            if abs(delta) < LIGHTING_CUTOFF:
                return(0)
            #print(self.level)
        return(1)
        #if self.level <= LIGHTING_CUTOFF:
            


class World():
    
    def __init__(self,width,height,tileManager) -> None:
        self.world = Matrix(width,height)
        self.width = width
        self.height = height
        self.lightingWorkloads = []
        self.tileManager = tileManager
        self.lightingInterface = None
        
    def caveGen(self,x,y,seed1, seed2, weight):
        data = noise.snoise2(x/50 + seed1,y/50 + seed2) + weight
        if data > 0:
            return(1)
        else:
            return(0)
    


    def spawnRare(self,x,y,seed,weight,freq):
        data = noise.snoise3(x/freq,y/freq, seed) + weight
        if data > 0:
            return(1)
        else:
            return(0)



        
    def genWorld(self):
        seed1 = random.randint(0,50)
        seed2 = random.randint(0,50)
        seed3 = random.randint(0,90)
        seed4 = 50#random.randint(40,80)
        caveSeed1 = random.randint(0,100000) 
        caveSeed2 = random.randint(0,100000)
        gradient = 60/self.height


        ironSeed = random.randint(0,90)
        
        for x in range(self.width):
            height = round(abs(noise.snoise2(x/50,seed2))*8) + round(abs(noise.snoise2(x/120,seed1))*8) + round(abs(noise.snoise2(x/1000,seed3))*30) + 200
            
            
            #print(height)
            
            for y in range(self.height):
                cell = Cell()
                #cell.tile = tiles.Tile()


                self.world[x,y] = cell
                
                
                if y < height:

                    
                    cell.backgroundTile = self.tileManager.fastCopy("air")
                    #cell.tile.sunlight = cell.tile.sunlightEmissive
                   
                elif y == WORLD_HEIGHT-1:
                    cell.tile = self.tileManager.fastCopy("bedrock")
                    #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive


                
                elif y < UNDERGROUND_END:   #code for underground

                    if y < UNDERGROUND_END-120:
                        cell.backgroundTile = self.tileManager.fastCopy("air") 
                    else:
                        cell.backgroundTile = self.tileManager.fastCopy("dirtBackground") 

                    if self.caveGen(x,y,caveSeed1,caveSeed2,.4):
                        #print("aaaa",cellTile,self.world[x,y-1].tile.tileName)
                        if self.spawnRare(x,y,ironSeed,-.5,5):
                            cell.tile = self.tileManager.fastCopy("iron")
                            
                            #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive
                        else:
                            if y == height:
                                cell.tile = self.tileManager.fastCopy("grass")
                            else:
                                cell.tile = self.tileManager.fastCopy("dirt")
                            
                            #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive

                        



                    #else:
                        
                        #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive
                        

                elif y < UNDERGROUND_END + 24: #transition period
                    block = random.randint(0,round(24/((y-UNDERGROUND_END)+1))  )

                    # if block == 0:
                           
                    #     cell.backgroundTile = self.tileManager.fastCopy("stoneBackground")
                    #         #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive

                    # else:
                            
                    cell.backgroundTile = self.tileManager.fastCopy("dirtBackground")


                    if self.caveGen(x,y,caveSeed1,caveSeed2,.5 - (y-UNDERGROUND_END)*.025):
                        

                        if block == 0:
                            cell.tile = self.tileManager.fastCopy("stone")
                            #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive
                            
                        else:
                            cell.tile = self.tileManager.fastCopy("dirt")
                            #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive
                            



                    
                        
                            #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive

                else: #code for caves
                    cell.backgroundTile = self.tileManager.fastCopy("stoneBackground")
                    if self.caveGen(x,y,caveSeed1,caveSeed2,.025):
                        
                        cell.tile = self.tileManager.fastCopy("stone")
                        #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive
                    
                        
                        
                        #cell.tile.sunlight = self.world[x,y-1].tile.sunlight *cell.tile.translucency + cell.tile.sunlightEmissive






                #compute sunlighting


                if y > 0:
                    tile = cell.tile
                    if not tile:
                        tile = cell.backgroundTile
                    #translucency = tile.translucency

                    cell.lighting.sunlight = self.world[x,y-1].lighting.sunlight * tile.translucency + tile.sunlightEmissive
                


    def __getitem__(self,loc):
        x,y = loc
        return(self.world[x,y])
    
    def __setitem__(self,loc,value):
        x,y = loc
        self.world[x,y] = value
        pass
    
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


    def inRange(self,x,y):
        if x > 0 and x < self.width-1:
            if y > 0  and y < self.height -1:
                return(True)

    


    def workOnlighting(self,lightingWorkload,buffers):

        done = False

        if type(lightingWorkload) == lightingWorkloadSunlight:
            #print("sunlight")
            level = lightingWorkload.step(buffers)
            if level < LIGHTING_CUTOFF:
                done = True





        
        else:
            originX =lightingWorkload.x
            originY =lightingWorkload.y
            
            


            offset = 0
            for i in range(len(lightingWorkload.rays)):
                cray = lightingWorkload.rays[i-offset]
                level = cray.step(1,buffers)
                if not level:
                    #print("killing")
                    del lightingWorkload.rays[i-offset]
                    offset += 1
            if len(lightingWorkload.rays) == 0:
                done = True
                #print("done")



        return(done)


    def workOnWorkloads(self,count,buffers):
        if len(self.lightingWorkloads) > 0:
            
            for i in range(count):
                
                if len(self.lightingWorkloads) == 0:
                    break
                #print("work load")
                workloadIndex = i%len(self.lightingWorkloads)
                workload = self.lightingWorkloads[workloadIndex]
                done = self.workOnlighting(workload,buffers)
                if done:
                    del self.lightingWorkloads[workloadIndex]


    def updateLighting(self,x,y,tile):
        

        
        self.lightingInterface.sendEvent(x,y)
        workload = lightingWorkloadSunlight(x,y,self)
        self.lightingWorkloads.append(workload)
            






    
