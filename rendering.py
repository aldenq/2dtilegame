from helpers import *
import pygame
from settings import *
import math
class Buffer():
    def __init__(self,width,height) -> None:
        self.buffer = pygame.Surface((width, height))
        pass
    

class BufferMatrix():

    def __init__(self,world,width,height) -> None:

        """
        Args:
            world: world object to create buffer matrix of
            width: amount of buffers to create in x
            height: amount of buffers to create in y
        
        
        
        
        """

        self.width = width
        self.height = height
        self.world=world
        self.buffers = Matrix(width,height)

        self.bufferWidth = int((world.width * TILE_WIDTH)/width) #pixels in a buffer
        self.bufferHeight = int((world.height * TILE_HEIGHT)/height)

        self.toBlit = []
        self.bufferTileX = int(world.width/width) #tiles in a buffer
        self.bufferTileY = int(world.height/height)

        for x in range(width):
            for y in range(height):
                self.buffers[x,y] = pygame.Surface((self.bufferWidth, self.bufferHeight))
    

    def drawBuffer(self,x,y):
        """
        Args:
            x: position in buffer matrix in x
            y: position in buffer matrix in y
        
        """
        
        offsetX = self.bufferTileX*x
        offsetY = self.bufferTileY*y
        buffer = self.buffers[x,y]
        
        #buffer.fill((255,0,255))



        lighting = pygame.Surface((TILE_WIDTH,TILE_HEIGHT))
        lighting.set_alpha(50)
        for localX in range(self.bufferTileX):
            for localY in range(self.bufferTileY):
                globalX = localX+offsetX
                globalY = localY+offsetY
                tile = self.world[globalX,globalY]
                #print(tile)
                




                red = int(tile.tile.color.r * (tile.tile.sunlight + tile.lighting.lighting.r))
                if red > 255: red = 255
                green = int(tile.tile.color.g * (tile.tile.sunlight + tile.lighting.lighting.g))
                if green > 255: green = 255
                blue = int(tile.tile.color.b *(tile.tile.sunlight + tile.lighting.lighting.b))
                if blue>255: blue = 255
                #print(red,green,blue, tile.color,globalX,globalY)


                if tile.tile.image == None:
                    pygame.draw.rect(buffer,(red,green,blue),(localX*TILE_WIDTH,localY * TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT))
                else:
                    lighting.fill((red*2 if red*3 < 255 else 255 ,green*3 if green*3 < 255 else 255,blue*3 if blue*3 < 255 else 255))
                    buffer.blit(tile.tile.image, (localX*TILE_WIDTH,localY * TILE_HEIGHT))
                    buffer.blit(lighting, (localX*TILE_WIDTH,localY * TILE_HEIGHT))
                    #pygame.draw.rect(buffer,(red,green,blue,1),(localX*TILE_WIDTH,localY * TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT))


    def updateTile(self,x,y):
        bufferx,buffery = self.getBuffer(x,y)
        tile = self.world[x,y]
        buffer = self.buffers[bufferx,buffery]

        localX = x-self.bufferTileX*bufferx
        localY = y-self.bufferTileY*buffery

        #summedLight = tile.sunlight + tile.lightLevel
        #pygame.draw.rect(buffer,(tile.r * summedLight,tile.g * summedLight,tile.b * summedLight),(localX*TILE_WIDTH,localY * TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT))
        
        red = tile.tile.color.r * (tile.tile.sunlight + tile.lighting.lighting.r)
        if red > 255: red = 255
        green = tile.tile.color.g * (tile.tile.sunlight + tile.lighting.lighting.g)
        if green > 255: green = 255
        blue = tile.tile.color.b *(tile.tile.sunlight + tile.lighting.lighting.b)
        if blue>255: blue = 255
        pygame.draw.rect(buffer,(red,green,blue),(localX*TILE_WIDTH,localY * TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT))
        pass
    
    def getBuffer(self,x,y): #returns what buffer a tile belongs to
        return((int(x/self.bufferTileX), int(y/self.bufferTileY)))

    def getBufferPoint(self,x,y):
        return((int(x/self.bufferWidth),int(y/self.bufferHeight)))

    def drawBuffers(self):
        for bufferX in range(self.width):
            for bufferY in range(self.height):
                self.drawBuffer(bufferX,bufferY)

    def blitBuffer(self,surface,bufferX,bufferY,offsetX,offsetY):
        surface.blit(self.buffers[bufferX,bufferY],(bufferX*self.bufferWidth - offsetX,bufferY*self.bufferHeight-offsetY))

    def blitBuffers(self,surface,camera):
        offsetX = camera.x
        offsetY = camera.y
        tlx,tly = camera.getGlobal(0,0)
        tlBufferX,tlBufferY = self.getBufferPoint(tlx,tly)


        brx,bry = camera.getGlobal(SCREEN_WIDTH,SCREEN_HEIGHT)
        brBufferX,brBufferY = self.getBufferPoint(brx,bry)
        
        
        if brBufferX < 0: brBufferX = 0
        if brBufferY < 0: brBufferX = 0
        #print((tlBufferX,tlBufferY),(brBufferX,brBufferY))

        if not (camera.lastX == camera.x and camera.lastY == camera.y):
            
        
            self.toBlit = []
            for bufferX in range(tlBufferX,brBufferX+1):
                
                for bufferY in range(tlBufferY,brBufferY+1):
                    self.toBlit.append((self.buffers[bufferX,bufferY],(bufferX*self.bufferWidth - offsetX,bufferY*self.bufferHeight-offsetY)))
        surface.blits(self.toBlit)
        camera.lastX = camera.x
        camera.lastY = camera.y


        
                #self.blitBuffer(surface, bufferX,bufferY,offsetX,OffsetY)
                





        
        pass


class Camera():
    def __init__(self,x,y) -> None:

        self.x = x
        self.y = y
        self.lastX = None
        self.lastY = None
        pass
    

    def getGlobal(self,x,y):
        return(x+self.x, y+self.y)
    def getOnscreen(self,x,y):
        return(x-self.x, y-self.y)

    def draw(self,surface,buffers):
        buffers.blitBuffers(surface,self)

