from settings import *
import pygame,math
from helpers import *
class Collider():
    def __init__(self,x,y,width,height, visible=False) -> None:
        self.physicsResolution = 10

        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0

        self.noClip = False
        self.hasGravity = True
        self.onGround = False
        self.canClimb = False

        self.lastX = x
        self.lastY = y

        self.width = width
        self.height = height
        self.visible = visible



        pass

    def moveTo(self,x,y):
        self.x = x
        self.y = y

    



    def runPhysics(self,world):
        if self.hasGravity:
            self.ySpeed += GRAVITY
        self.lastX = self.x
        ystep = math.ceil(abs(self.ySpeed/self.physicsResolution)) * sign(self.ySpeed)

        self.onGround = 0
        #print(self.checkCollision(world))

        if ystep != 0:
            repeats = math.ceil(self.ySpeed/ystep)
        else:
            repeats = 0
        #print(repeats)
        

        for i in range(repeats):
            self.lastY = self.y
            self.y += ystep
            if self.checkCollision(world):
                self.y = self.lastY
                self.ySpeed = 0


                if ystep > 0:
                    self.onGround = 1
                break
                

        
            
        xstep = math.ceil(abs(self.xSpeed/self.physicsResolution)) * sign(self.xSpeed)
        #print(xstep)

        if xstep != 0:
            repeats = math.ceil(self.xSpeed/xstep)
        else:
            repeats = 0
        #print(repeats)
        for i in range(repeats):
            self.lastX = self.x
            self.x += xstep



            if self.checkCollision(world):
                if self.canClimb == True and self.onGround == True:
                    self.y -= TILE_HEIGHT
                    if self.checkCollision(world):
                        self.y += TILE_HEIGHT
                        #print("jump failed")
                    else:
                        continue


                self.x = self.lastX
                break


        



        






    def draw(self,surface, camera):
        x,y = camera.getOnscreen(self.x,self.y)
        pygame.draw.rect(surface, (255,0,255), (x,y,self.width,self.height))


    def checkCollision(self,world):
        topLeftX,topLeftY = world.getBlock(self.x,self.y)
        bottomRightX,bottomRightY = world.getBlock(self.x + self.width,self.y+self.height)
        #print(topLeftX,topLeftY,bottomRightX,bottomRightY )
        topLeftX -= 1
        topLeftY -= 1

        bottomRightX += 2
        bottomRightY += 2

        for x in range(topLeftX,bottomRightX):
            for y in range(topLeftY,bottomRightY):
                tile = world[x,y].tile
                if not tile:
                    continue
                if not tile.isSolid:
                    continue
                
                tileTLX, tileTLY = world.getPos(x,y)
                tileBRX = tileTLX + TILE_WIDTH
                tileBRY = tileTLY + TILE_HEIGHT


                #print(topLeftX,tileTLX)

                #print(f"{tileTLX},{tileTLY} {tileBRX},{tileBRY}")
                #print(f"{self.x},{self.y}  {self.y+self.height},{self.x+self.width}")
                #if (self.x >= tileTLX and self.x <= tileBRX) or (self.x+self.width >= tileTLX and self.x+self.width <= tileBRX):
                    
                    #if (self.y > tileTLY and self.y <= tileBRY) or (self.y+self.height > tileTLY and self.y+self.height <= tileBRY):
                
                if(self.x >= tileBRX or tileTLX >= self.x+self.width):
                    #print("failed first")  
                    continue
                if(self.y+self.height <= tileTLY or tileBRY <= self.y):
                    #print("failed second")
                    continue
                
                return(True)

        return(False)
    def checkOverlap(self,other):
        if(self.x >= other.x+other.width or other.x >= self.x+self.width):
            return(False)
        if(self.y+self.height <= other.y or other.y+other.height <= self.y):
            return(False)
                
        return(True)


