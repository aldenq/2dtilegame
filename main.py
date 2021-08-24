
import pygame
from pygame.locals import *

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
print("generating terrain...")
st = time.time()
world = World(WORLD_WIDTH,WORLD_HEIGHT)
print(f"took: {time.time()-st}")
print(f"drawing buffers")

buffers = rendering.BufferMatrix(world,5,5)
buffers.drawBuffers()

entityManager = entities.EntityManager(world)

mytool = tools.Tool("test tool")

mainPlayer = player.Player(50,50)
mainPlayer.fly = False
mainPlayer.collider.hasGravity = True



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
 
# initialize pygame
print("init")
pygame.init()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
 
# create a window
flags =  DOUBLEBUF

screen = pygame.display.set_mode(screen_size,flags)
screen.set_alpha(None)

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
    


    if pygame.mouse.get_pressed()[0]:
        x,y = pygame.mouse.get_pos()
        globalX,globalY = mainPlayer.camera.getGlobal(x,y)
        mainPlayer.tool.leftClick(globalX,globalY)
    

    if pygame.mouse.get_pressed()[2]:
        x,y = pygame.mouse.get_pos()
        globalX,globalY = mainPlayer.camera.getGlobal(x,y)
        mainPlayer.tool.rightClick(globalX,globalY)








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
def startGame():
    global running,st
    
    #print("starting")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        #clear the screen
        screen.fill((100,100,200))



        #print(1/(time.time()-st))
        #st = time.time()
        #print(pygame.mouse.get_pos())
        #screen.blit(buffers.buffers[0,0],(0,0))
        mx,my = pygame.mouse.get_pos()
        gx,gy = mainPlayer.camera.getGlobal(mx,my)
        blockX,blockY = world.getBlock(gx,gy)
        #print(blockX,blockY)
        #print(world[blockX,blockY].lighting.passthroughs)



        world.workOnWorkloads(8,buffers)
        input()

        #st2 = time.time()
        
        mainPlayer.showView(screen,buffers)
        #print(time.time()-st2)
        entityManager.drawEntities(screen,mainPlayer.camera)
        mainPlayer.applyPhysics(world)
        entityManager.simulateEntities()
        
            
        

            
            #
            
            
            #
            
            
            #mainPlayer.collider.draw(screen,mainPlayer.camera)
        pygame.display.flip()
        #print(time.time()-st2)

        
        # how many updates per second
        #clock.tick(60)
#print(__name__ == "__main__")
#if __name__ == "__main__":
#startGame()
#pygame.quit()









