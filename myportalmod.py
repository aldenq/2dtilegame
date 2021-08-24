
from player import Player
import main
import pygame

from entities import Entity
from tools import Tool
import time


def spawnRedPortal(item,x,y): 
    global redPortal
    redPortal.visible = True
    redPortal.x = x
    redPortal.y = y
    #print("red")
    pass

def spawnBluePortal(item,x,y):
    global bluePortal
    bluePortal.visible = True
    bluePortal.x = x
    bluePortal.y = y
    #print("blue")
    pass


lastTeleport = time.time()
teleportCooldown = .1

def playerBehavior(player):
    global lastTeleport
    #print(player.x,"test")
    if time.time()-lastTeleport > teleportCooldown: #check if teleport cooldown has runout
        overlaps = main.entityManager.getCollisions(player.collider) #get all entities which the player overlaps with

        for entity in overlaps: 
            if entity.id == "red": 
                player.x = bluePortal.x
                player.y = bluePortal.y
                lastTeleport = time.time()
            if entity.id == "blue":
                player.x = redPortal.x
                player.y = redPortal.y
                lastTeleport = time.time()
        
    pass

def drawRedPortal(entity, surface, camera):
    screenX,screenY = camera.getOnscreen(entity.x,entity.y) #convert the global cords where 0,0 is the top left of the world into local cords where 0,0 is the top left of the screen
    pygame.draw.rect(surface,(255, 85, 13),(screenX,screenY,entity.width,entity.height))

def drawBluePortal(entity, surface, camera):
    screenX,screenY = camera.getOnscreen(entity.x,entity.y)
    pygame.draw.rect(surface,(0, 100, 255),(screenX,screenY,entity.width,entity.height))





portalGun = Tool("portal gun") #create a new tool called "portal gun"
portalGun.leftAction = spawnRedPortal #set left click behavior to spawn red portal
portalGun.rightAction = spawnBluePortal #set right click behavior to spawn blue portal
main.mainPlayer.tool = portalGun #equip the player with this new tool


redPortal = Entity(0,0,0,0,4,30) #create entity that will be used for red portal
redPortal.id = "red"
redPortal.draw = drawRedPortal #define drawing behavior
redPortal.collider.hasGravity = False
redPortal.visible = False


bluePortal = Entity(0,0,0,0,4,30)
bluePortal.id = "blue"
bluePortal.collider.hasGravity = False
bluePortal.visible = False
bluePortal.draw = drawBluePortal




main.entityManager.spawn(redPortal) #spawn the entities
main.entityManager.spawn(bluePortal)


main.mainPlayer.AI = playerBehavior #add new portal teleporting behavior to the player

#redPortal = Entity(0,0,)




main.startGame()









