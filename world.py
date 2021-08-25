
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
        self.lighting = Color(0,0,0)
        self.passthroughs = []
        pass


class Cell():
    """
    used to store all information relating to tiles
    
    """
    def __init__(self) -> None:
        self.lighting = lightingData()
        self.tile = None
        pass

    



class ray():
    """
    creates a ray that can be used to calculate volumetrics and lighting
    
    """
    speed = TILE_WIDTH/4
    def __init__(self,originX,originY,angle,intensity,r,g,b,world) -> None:
        self.color = (Color(r,g,b)/255)*intensity
        
        self.xspeed = math.cos(angle)*self.speed
        self.yspeed = math.sin(angle)*self.speed


        # testX = (self.xspeed * 100)//TILE_WIDTH
        # if testX != 0:
        #     testY = ((self.yspeed * 100)//TILE_HEIGHT)/testX
        #     self.xspeed = TILE_WIDTH#*= self.speed
        #     self.yspeed = testY
        

        # if abs(self.xspeed) > abs(self.yspeed):
        #     self.speed = TILE_WIDTH/abs(self.xspeed) 
        # else:
        #     self.speed = TILE_WIDTH/abs(self.yspeed)
        
        #self.speed /= 2
        
        
        #print(self.xspeed,self.yspeed,self.speed)
        self.x,self.y = world.getPos(originX,originY)

        self.x += TILE_WIDTH/2
        self.y += TILE_HEIGHT/2

        self.origin = (originX,originY)
        self.intensity = intensity
        self.world = world
        self.lastTileX = 0
        self.lastTileY = 0
        self.tile = None


    def step(self,count,buffers):
        tileX,tileY = 0,0
        #print("sim")
        for i in range(count):
            
            #self.x += self.xspeed
            #self.y += self.yspeed
            tileX,tileY = self.world.getBlock(self.x,self.y)
            
            

            #print(self.color,self.x,self.y)

            
            #print(tileX,tileY,"tile")

            if self.x < 0 or self.x > WORLD_WIDTH*TILE_WIDTH:
                #print("out of bounds x")
                return(0)
            if self.y < 0 or self.y > WORLD_HEIGHT*TILE_HEIGHT:
                #print("out of bounds y")
                return(0)

            
            #print("doing stuff")
            self.tile = self.world[tileX,tileY]
            
            #self.color *= tile.tile.translucency
            clone = copy.copy(self)
            clone.color = copy.copy(self.color)

            self.tile.lighting.passthroughs.append(clone)
            self.lastTileX = tileX
            self.lastTileY = tileY

            while self.lastTileX == tileX and self.lastTileY == tileY:
                #print("repeat")
                self.color.r = self.color.r*(1-self.tile.tile.colorTranslucency.r)
                self.color.g = self.color.g*(1-self.tile.tile.colorTranslucency.g)
                self.color.b = self.color.b*(1-self.tile.tile.colorTranslucency.b)
                #print(self.color,tile.tile.colorTranslucency, )
                self.tile.lighting.lighting.r += self.color.r
                self.tile.lighting.lighting.g += self.color.g
                self.tile.lighting.lighting.b += self.color.b
                self.x += self.xspeed
                self.y += self.yspeed
                tileX,tileY = self.world.getBlock(self.x,self.y)
            
            buffers.updateTile(self.lastTileX ,self.lastTileY )
            

            
        #print("raying and tracing", self.x,self.y,self.xspeed,self.yspeed,self.intensity)
        return(self.color.r + self.color.g + self.color.b)
    #def reStep(self,count, buffers):






        

        #self.origin
        pass
    

    
    
    
class lightingWorkload():
    
    def __init__(self,x,y,level,count,world):
        self.x = x
        self.y = y
        self.level = level
        self.radius = 0
        self.rays = []


        for i in range(count):
            self.rays.append(   ray(x,y, (6.283/count) *i,level ,255,255,255,world   )                          )






class World():
    
    def __init__(self,width,height) -> None:
        self.world = Matrix(width,height)
        self.width = width
        self.height = height
        self.genWorld()
        self.lightingWorkloads = []

        
    def caveGen(self,x,y,seed1, seed2, weight):
        data = noise.snoise2(x/50 + seed1,y/50 + seed2) + weight
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
        
        for x in range(self.width):
            height = round(abs(noise.snoise2(x/50,seed2))*8) + round(abs(noise.snoise2(x/120,seed1))*8) + round(abs(noise.snoise2(x/1000,seed3))*30) + 200
            
            
            #print(height)
            
            for y in range(self.height):
                cell = Cell()
                #cell.tile = tiles.Tile()


                self.world[x,y] = cell
                
                
                if y < height:

                    
                    cell.tile = tiles.tileManager.fastCopy("air")
                   
                
                elif y < UNDERGROUND_END:   #code for underground
                    if self.caveGen(x,y,caveSeed1,caveSeed2,.5):
                        #print("aaaa",cellTile,self.world[x,y-1].tile.tileName)
                        cell.tile = tiles.tileManager.fastCopy("dirt")
                        
                        cell.tile.sunlight = self.world[x,y-1].tile.sunlight *.9


                    else:
                        cell.tile = tiles.tileManager.fastCopy("dirtBackground")
                        cell.tile.sunlight = self.world[x,y-1].tile.sunlight
                        

                elif y < UNDERGROUND_END + 24: #transition period
                    block = random.randint(0,round(24/((y-UNDERGROUND_END)+1))  )
                    if self.caveGen(x,y,caveSeed1,caveSeed2,.5 - (y-UNDERGROUND_END)*.025):
                        

                        if block == 0:
                            cell.tile = tiles.tileManager.fastCopy("stone")
                            cell.tile.sunlight = self.world[x,y-1].tile.sunlight *.9
                            
                        else:
                            cell.tile = tiles.tileManager.fastCopy("dirt")
                            cell.tile.sunlight = self.world[x,y-1].tile.sunlight *.9
                            



                    else:
                        if block == 0:
                           
                            cell.tile = tiles.tileManager.fastCopy("stoneBackground")
                            cell.tile.sunlight = self.world[x,y-1].tile.sunlight

                        else:
                            
                            cell.tile = tiles.tileManager.fastCopy("dirtBackground")
                            cell.tile.sunlight = self.world[x,y-1].tile.sunlight

                else: #code for caves
                    if self.caveGen(x,y,caveSeed1,caveSeed2,-.1):
                        
                        cell.tile = tiles.tileManager.fastCopy("stone")
                        cell.tile.sunlight = self.world[x,y-1].tile.sunlight *.9
                    else:
                        
                        cell.tile = tiles.tileManager.fastCopy("stoneBackground")
                        cell.tile.sunlight = self.world[x,y-1].tile.sunlight

        #print("done")


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
        originX =lightingWorkload.x
        originY =lightingWorkload.y
        
        done = False


        offset = 0
        for i in range(len(lightingWorkload.rays)):
            cray = lightingWorkload.rays[i-offset]
            level = cray.step(1,buffers)
            if level < LIGHTING_CUTOFF:
                #print("killing")
                del lightingWorkload.rays[i-offset]
                offset += 1
        if len(lightingWorkload.rays) == 0:
            done = True
            #print("done")








        




        
        
        return(done)
            
        pass

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

        if tile.emissionlevel > 0:
            workload = lightingWorkload(x,y,tile.emissionlevel,145,self)
            self.lightingWorkloads.append(workload)
        else:
            workload = lightingWorkload(x,y,0,0,self)
            workload.rays = []
            for i in self.world[x,y].lighting.passthroughs:
                out = copy.copy(i)
                out.color = copy.copy(i.color)
                workload.rays.append(out)
            #= copy.deepcopy(self.world[x,y].lighting.passthroughs)
            #for i in workload.rays:
            #    i = cop
            self.lightingWorkloads.append(workload)
            #print(self.lightingWorkloads[0].rays)
            






    
