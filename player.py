from helpers import Matrix
import copy
from settings import *
import physics,rendering,pygame
class Player():
    def __init__(self,x,y) -> None:
        self.x = y
        self.y = x

        self.xspeed = 0
        self.yspeed = 0

        self.health = 20
        self.hunger = 20
        self.width = TILE_WIDTH * 1.4
        self.height = TILE_HEIGHT * 3

        self.onGround = False
        self.camera = rendering.Camera(self.x,self.y)
        self.collider = physics.Collider(x,y,self.width,self.height)
        self.collider.canClimb = True
        self.collider.hasGravity = True

        self.hotbarSelect = 0
        self.inventory = Inventory(self)
        self.tool = None
        self.AI = None
        self.fly = False

        pass
    
    def applyPhysics(self,world):
        if callable(self.AI):
            self.AI(self)
            
        self.collider.x = self.x
        self.collider.y = self.y
        #print(self.xspeed,self.yspeed)
        self.collider.xSpeed = self.xspeed
        self.collider.ySpeed = self.yspeed
        #print(self.yspeed)
        #print(self.xspeed)
        self.collider.runPhysics(world)

        self.x = self.collider.x
        self.y = self.collider.y

        self.yspeed = self.collider.ySpeed
        self.xspeed = self.collider.xSpeed

        self.camera.x = self.x - (SCREEN_WIDTH/2 - self.width/2)
        self.camera.y = self.y - (SCREEN_HEIGHT/2 - self.height/2)
        self.onGround = self.collider.onGround

    def draw(self,surface):
        pygame.draw.rect(surface, (100,25,20), (SCREEN_WIDTH/2 - self.width/2,SCREEN_HEIGHT/2 - self.height/2,self.width,self.height))
        pass

    def drawCursor(self,surface,mouseX,mouseY,world):
        globalX,globalY = self.camera.getGlobal(mouseX,mouseY)
        blockX,blockY = world.getBlock(globalX,globalY)
        red = 106
        green = 198
        blue = 247
        #print(self.tool)
        if self.tool != None and self.tool.maxRange != 0:
            
            


            globalX2,globalY2 = self.camera.getGlobal(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
            blockX2,blockY2 = world.getBlock(globalX2,globalY2)

            
            toolRange = self.tool.maxRange

            dist = ((blockX-blockX2)**2 + (blockY-blockY2)**2)**.5

            if dist > toolRange:
                red = 232
                green = 58 
                blue = 5
                self.tool.outOfRange = True
            else:
                self.tool.outOfRange = False



        blockPXX,blockPXY = world.getPos(blockX,blockY)
        drawX,drawY = self.camera.getOnscreen(blockPXX,blockPXY)


        pygame.draw.rect(surface,(red, green, blue),(drawX,drawY,TILE_WIDTH,TILE_HEIGHT),2)


    def showView(self,surface,buffers):
        
        self.camera.draw(surface,buffers)
        self.draw(surface)

    
    def selectTool(self,index):
        self.tool = self.inventory[index,0]
        self.hotbarSelect = index






class Inventory:

    """
    
    used to store information about the players inventory
    
    """


    def __init__(self,owner) -> None:
        self.items = Matrix(INVENTORY_WIDTH,INVENTORY_HEIGHT)
        self.owner = owner
        pass
    

    def __getitem__(self,loc):
        return(self.items[loc])


    def __setitem__(self,loc,item):
        self.items[loc] = item
    
    def __repr__(self) -> str:
        return(str(self.items))
        pass
    


    def manageInventory(self):
        for y in range(INVENTORY_HEIGHT):
            for x in range(INVENTORY_WIDTH):
                if self.items[x,y] != 0:
                    if self.items[x,y].count <= 0:
                        self.items[x,y] = 0
                        if y == 0 and self.owner.hotbarSelect == x:
                            self.owner.tool = None
                        

    def giveItem(self,item,count = 1):
        lastFree = 0
        for y in range(INVENTORY_HEIGHT):
            for x in range(INVENTORY_WIDTH):
                if self.items[x,y] == 0:

                    if not lastFree:
                        lastFree = (x,y)

                    if item.stackable == False:
                        self.items[x,y] = copy.copy(item)
                        self.items[x,y].user = self.owner
                        return()

                elif self.items[x,y].name == item.name and item.stackable:
                    self.items[x,y].count += count
                    return()
        x,y = lastFree
        self.items[x,y] = copy.copy(item)
        self.items[x,y].user = self.owner
        self.items[x,y].count = count

                    #print("giving item")
                    

    
    
    


    


    


    

    
    



    






    
    





