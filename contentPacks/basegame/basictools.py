import pygame
mainPlayer = None
world = None
buffers = None
tileManager = None
entityManager = None
screen = None
Tool = None
itemManager = None




	

def mineBlock(item,x,y):
    if not item.outOfRange:
       blockX,blockY = world.getBlock(x,y)
       if world[blockX,blockY].tile.tileName != "air" and not world[blockX,blockY].tile.unbreakable :
           #print(world[blockX,blockY].tile.drops)
           #print(item.user.inventory)
           if world[blockX,blockY].tile.drops:
                item.user.inventory.giveItem(itemManager[world[blockX,blockY].tile.drops])
           world[blockX,blockY].tile = tileManager["air"]
        
        
           buffers.updateTile(blockX,blockY)
           world.updateLighting(blockX,blockY,tileManager["air"])





def addContent():

	pickaxe = Tool("pickaxe")
	pickaxe.leftAction = mineBlock
	pickaxe.icon = pygame.image.load("contentPacks/basegame/assets/pickaxe.bmp")
	pickaxe.maxRange = 6
	#print(itemManager.items)
	itemManager["pickaxe"] = pickaxe
	
	



