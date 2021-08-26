
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
import sys

from multiprocessing import Process, Value, Array, Lock,Queue



pygame.init()
screen_size = (SCREEN_WIDTH*SCALE, SCREEN_HEIGHT*SCALE)
 
flags =   DOUBLEBUF

screen = pygame.display.set_mode(screen_size,flags)
#screen.set_alpha(None)
print("loading in content packs")


print("generating terrain...")
st = time.time()
world = World(WORLD_WIDTH,WORLD_HEIGHT)
print(f"took: {time.time()-st}")
print(f"drawing buffers")

buffers = rendering.BufferMatrix(world,5,5)
buffers.drawBuffers()
print("done")
entityManager = entities.EntityManager(world)
itemManager = tools.ItemManager()


mainPlayer = player.Player(1000,1000)
mainPlayer.fly = False
mainPlayer.collider.hasGravity = True

INTERLACE_COUNT = 2
INTERLACE_HEIGHT = SCREEN_HEIGHT/INTERLACE_COUNT
RENDER_TARGET_FPS = 60

def render(update,event,lock,events,fps,mouseX,mouseY,frameReady):
    st = time.time()
    odd = False
    
    while True:
        #screen.flip()
        #lock.acquire()
        print(fps.value)
        fps.value = int(1/(time.time()-st))
        st = time.time()
        while not frameReady.value:
            pass

        # for i in range(int(INTERLACE_COUNT/2)): #interlacer
        #      #print("rendering")
        #     update((0,((i)*2 + odd) * INTERLACE_HEIGHT-1,SCREEN_WIDTH, INTERLACE_HEIGHT+1))
        
        update()
        odd = not odd
        mx,my = pygame.mouse.get_pos()

        mouseX.value = mx
        mouseY.value = my
        for i in pygame.event.get():
            events.put((i.type,i.dict))

        #for i in range(len(pygame.key.get_pressed())):
        #  keys[i] = pygame.key.get_pressed()[i]
        # #print(list(keys))

        
        stime = (1/RENDER_TARGET_FPS)-(time.time()-st)   
        time.sleep(stime if stime > 0 else 0 )
        #lock.release()
        #print()   







#content packs
######################
#this is just a ridiculous scheme for avoiding circular imports, will come up with better solution later.
import contentPacks.basegame.basicBlocks as basicBlocks
basicBlocks.mainPlayer = mainPlayer
basicBlocks.buffers = buffers
basicBlocks.world = world
basicBlocks.entityManager = entityManager
basicBlocks.tileManager = tiles.TileManager
basicBlocks.screen = screen
basicBlocks.addContent()

import contentPacks.basegame.basictools as basictools
basictools.mainPlayer = mainPlayer
basictools.buffers = buffers
basictools.world = world
basictools.entityManager = entityManager
basictools.tileManager = tiles.tileManager
basictools.screen = screen
basictools.Tool = tools.Tool
basictools.itemManager = itemManager
basictools.addContent()

import contentPacks.basegame.basicEntities as basicEntities

mainPlayer.tool = itemManager["pickaxe"]

#######################






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
    #keys=pygame.key.get_pressed()
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
    



keys = list(pygame.key.get_pressed())

lock = Lock()
fps = Value('i', 0)
mouseX = Value('i', 0)
mouseY = Value('i', 0)
frameReady = Value('i',0)
eventQueue = Queue()
#keys =  pygame.key.get_pressed()#Array('i',list())
p = Process(target=render, args=(pygame.display.update,pygame.event,lock,eventQueue,fps,mouseX,mouseY,frameReady))
p.daemon = True
p.start()




st = time.time()
ast = time.time()
frame = 0
def startGame():
    global running,st,frame,keys
    
    #print("starting")
    while running:
        frame += 1
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #         pygame.quit()


        #print(pygame.K_a,"a key")
        while not eventQueue.empty():
            type,dict = eventQueue.get_nowait()
            if type == pygame.KEYDOWN:
                keys[dict["key"]] = 1
            if type == pygame.KEYUP:
                keys[dict["key"]] = 0

                #print(keys)
                #print(dict)
            if type == pygame.QUIT:
                print("quit")
    
            
        
        # #clear the screen
        # #screen.fill((100,100,200))



         #print(1/(time.time()-st))
        # #st = time.time()

        #print(frame/(time.time() - ast), 1/(time.time()-st)  )
        st = time.time()
        # #print(pygame.mouse.get_pos())
        # #screen.blit(buffers.buffers[0,0],(0,0))
        
        #print(mouseX.value,mouseY.value)
        # gx,gy = mainPlayer.camera.getGlobal(mx,my)
        # blockX,blockY = world.getBlock(gx,gy)
        # #print(blockX,blockY)
        # #print(world[blockX,blockY].lighting.passthroughs)



        world.workOnWorkloads(8,buffers)
        input()

        # #st2 = time.time()
        #print("aa")
        #frameReady.value = False
        frameReady.value = False
        mainPlayer.showView(screen,buffers)
        
        #print(time.time()-st2)
        entityManager.drawEntities(screen,mainPlayer.camera)
        mainPlayer.applyPhysics(world)
        entityManager.simulateEntities()
        frameReady.value = True
        
        
            
        

            
        #     #
            
            
        #     #
            
            
        #     #mainPlayer.collider.draw(screen,mainPlayer.camera)
        #pygame.display.flip()
        #print(time.time()-st2)

        
        
        clock.tick(60)
        
#print(__name__ == "__main__")
if __name__ == "__main__":
    startGame()
#pygame.quit()










