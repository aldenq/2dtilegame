
from standardActions import Actions
import pygame
import pygame.freetype
from pygame.locals import *
pygame.init()

import math
import time
import random


from helpers import *
from settings import *
from world import World
import tiles
import rendering
import physics
import player
import entities
import tools
import copy
import sys
import UI
import standardActions
screen_size = (SCREEN_WIDTH*SCALE, SCREEN_HEIGHT*SCALE)
 
flags =   DOUBLEBUF

screen = pygame.display.set_mode(screen_size,flags)
#screen.set_alpha(None)
tileManager = tiles.TileManager()

world = World(WORLD_WIDTH,WORLD_HEIGHT,tileManager)

buffers = rendering.BufferMatrix(world,5,5)

entityManager = entities.EntityManager(world)

itemManager = tools.ItemManager()



mainPlayer = player.Player(1000,1000)
mainPlayer.fly = False
mainPlayer.collider.hasGravity = True

actions = standardActions.Actions(world,buffers,mainPlayer,tileManager,itemManager,entityManager)
itemManager.standardActions=actions



# world, buffers, mainPlayer,tileManager,itemManager,entityManager

print("loading in content packs")



#content packs
######################
#this is just a ridiculous scheme for avoiding circular imports, will come up with better solution later.
import contentPacks.basegame.basicBlocks as basicBlocks
basicBlocks.mainPlayer = mainPlayer
basicBlocks.buffers = buffers
basicBlocks.world = world
basicBlocks.entityManager = entityManager
basicBlocks.tileManager = tileManager
basicBlocks.screen = screen
basicBlocks.Tile = tiles.Tile
basicBlocks.Tool = tools.Tool
basicBlocks.itemManager = itemManager
basicBlocks.addContent()

import contentPacks.basegame.basictools as basictools
basictools.mainPlayer = mainPlayer
basictools.buffers = buffers
basictools.world = world
basictools.entityManager = entityManager
basictools.tileManager = tileManager
basictools.screen = screen
basictools.Tool = tools.Tool
basictools.itemManager = itemManager
basictools.addContent()

import contentPacks.basegame.basicEntities as basicEntities

mainPlayer.tool = itemManager["pickaxe"]
mainPlayer.tool.user = mainPlayer
#######################








print("generating terrain...")
st = time.time()
world.genWorld()

print(f"took: {time.time()-st}")
print(f"drawing buffers")

buffers.drawBuffers()


print("done")












# def toolLeft(tool,x,y):
#     print(x,y)


# mytool.leftAction = toolLeft
# mainPlayer.tool = mytool

# def testAI(entity : entities.Entity):
#     #print(entity.x)
#     if entity.collider.onGround:
#         entity.yspeed = -40



# testEnt = entities.Entity(100,100,1,1,10,10)
# testEnt.AI = testAI

# entityManager.spawn(testEnt)







WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
print("init")

print(pygame.display.get_driver())
pygame.display.set_caption("pygame Test")
 
# clock is used to set a max fps
clock = pygame.time.Clock()
 

running = True




def input():
    global mainPlayer
    keys=pygame.key.get_pressed()
    #print(mainPlayer.xspeed)
    if keys[pygame.K_a]:
        mainPlayer.xspeed = -4
        #print("a")
    elif keys[pygame.K_d]:
        mainPlayer.xspeed = 4
        #print("d")
    else:
        mainPlayer.xspeed = 0
    

    if keys[pygame.K_w]:
        if mainPlayer.onGround:
            mainPlayer.yspeed = -15
    
    if mainPlayer.fly == True:
        if keys[pygame.K_w]:
            mainPlayer.yspeed = -4
        elif keys[pygame.K_s]:
            mainPlayer.yspeed = 4
        else:
            mainPlayer.yspeed = 0


    if keys[pygame.K_a] and keys[pygame.K_d]:
        mainPlayer.xspeed = 0
    

    if mainPlayer.tool:
        if pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos()
            globalX,globalY = mainPlayer.camera.getGlobal(x,y)
            mainPlayer.tool.leftClick(globalX,globalY)
        

        if pygame.mouse.get_pressed()[2]:
            x,y = pygame.mouse.get_pos()
            globalX,globalY = mainPlayer.camera.getGlobal(x,y)
            mainPlayer.tool.rightClick(globalX,globalY)


    if keys[pygame.K_1]:
       mainPlayer.selectTool(0)
    if keys[pygame.K_2]:
       mainPlayer.selectTool(1)
    if keys[pygame.K_3]:
       mainPlayer.selectTool(2)
    if keys[pygame.K_4]:
       mainPlayer.selectTool(3)
    if keys[pygame.K_5]:
       mainPlayer.selectTool(4)
    if keys[pygame.K_6]:
       mainPlayer.selectTool(5)
    if keys[pygame.K_7]:
       mainPlayer.selectTool(6)
    if keys[pygame.K_8]:
       mainPlayer.selectTool(7)







def setblock(x,y,tile):
        global world
        #blockX,blockY = world.getBlock(globalX,globalY)
        #newTile = Tile(214 + random.randint(-4,4), 147, 13)
        #newTile.isSolid = True
        world[x,y].tile = tile


        buffers.updateTile(x,y)
        world.updateLighting(x,y,tile)

        #print(blockX,blockY)
        #print("mouse down")



def setblocks(x,y,x1,y1,tile):
    
    global world
    #blockX,blockY = world.getBlock(globalX,globalY)
    #newTile = Tile(214 + random.randint(-4,4), 147, 13)
    #newTile.isSolid = True

    for x2 in range(x,x1):
        for y2 in range(y,y1):
            actualTile = copy.copy(tile)
            actualTile.color = copy.copy(tile.color)

            world[x2,y2].tile = actualTile


            buffers.updateTile(x2,y2)
            world.updateLighting(x2,y2,actualTile)

    #print(blockX,blockY)
    #print("mouse down")

st = time.time()
ast = time.time()
frame = 0




hotbar = UI.HotBar()





def startGame():
    global running,st,frame
    
    #print("starting")


    mainPlayer.inventory.giveItem(itemManager["pickaxe"])
    mainPlayer.inventory.giveItem(itemManager["bedrock"],count=100)
    #mainPlayer.inventory.giveItem(itemManager["pickaxe"])
    #mainPlayer.inventory.giveItem(itemManager["pickaxe"])
    print(mainPlayer.inventory)
    while running:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
        
        # #clear the screen
        # #screen.fill((100,100,200))



         #print(1/(time.time()-st))
        # #st = time.time()

        #print(frame/(time.time() - ast), 1/(time.time()-st)  )
        st = time.time()
        


        
        # #print(pygame.mouse.get_pos())
        # #screen.blit(buffers.buffers[0,0],(0,0))
        
        # gx,gy = mainPlayer.camera.getGlobal(mx,my)
        # blockX,blockY = world.getBlock(gx,gy)
        # #print(blockX,blockY)
        # #print(world[blockX,blockY].lighting.passthroughs)



        world.workOnWorkloads(8,buffers)
        input()

        # #st2 = time.time()
        mainPlayer.inventory.manageInventory()
        mainPlayer.showView(screen,buffers)
        mx,my = pygame.mouse.get_pos()
        mainPlayer.drawCursor(screen,mx,my,world )
        #print(time.time()-st2)
        hotbar.draw(mainPlayer,screen)
        entityManager.drawEntities(screen,mainPlayer.camera)
        mainPlayer.applyPhysics(world)
        entityManager.simulateEntities()
        
            
        

            
        #     #
            
            
        #     #
            
            
        #     #mainPlayer.collider.draw(screen,mainPlayer.camera)
        pygame.display.flip()
        #print(time.time()-st2)

        
        
        clock.tick(MAX_FPS)
#print(__name__ == "__main__")
if __name__ == "__main__":
    startGame()
#pygame.quit()










