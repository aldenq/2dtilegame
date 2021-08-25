mainPlayer = None
world = None
buffers = None
tileManager = None
entityManager = None
screen = None
Tool = None
itemManager = None




	

def mineBlock(item,x,y):
    blockX,blockY = world.getBlock(x,y)
    if world[blockX,blockY].tile.tileName != "air":
        world[blockX,blockY].tile = tileManager["air"]


        buffers.updateTile(blockX,blockY)
        world.updateLighting(blockX,blockY,tileManager["air"])





def addContent():

	pickaxe = Tool("pickaxe")
	pickaxe.leftAction = mineBlock
	print(itemManager.items)
	itemManager["pickaxe"] = pickaxe
	
	



