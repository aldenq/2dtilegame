import pygame
mainPlayer = None
world = None
buffers = None
tileManager = None
entityManager = None
screen = None
Tile = None
Tool = None
itemManager = None




def placeBlock(item,x,y):
    
    blockX,blockY = world.getBlock(x,y)
    if world[blockX,blockY].tile.tileName != "air":
        world[blockX,blockY].tile = tileManager["air"]
        buffers.updateTile(blockX,blockY)
        world.updateLighting(blockX,blockY,tileManager["air"])





def addContent():













	air = Tile(0,0,220)
	air.isSolid = False
	air.bRange = 5
	air.sunlight = 1
	air.translucency = .1
	air.rRange = 0
	air.bRange = 0
	air.gRange = 0
	air.image = pygame.image.load("assets/air.png")
	#air.darkenImage()
	tileManager["air"] = air


	dirt = Tile(117 , 76 ,19)
	dirt.isSolid = True
	dirt.tileID = 1
	dirt.rRange = 5
	dirt.bRange = 5
	dirt.translucency = .6
	dirt.image = pygame.image.load("assets/dirt.bmp")
	#dirt.darkenImage()
	tileManager["dirt"] = dirt


	dirtBackground = Tile(50,30,9)
	dirtBackground.isSolid = False
	dirtBackground.tileID = 0
	dirtBackground.rRange = 5
	dirtBackground.bRange = 5
	dirtBackground.translucency = .97

	dirtBackground.image = pygame.image.load("assets/dirtbackground.bmp")
	#dirtBackground.darkenImage()
	tileManager["dirtBackground"] = dirtBackground


	stone = Tile(70,70,80)
	stone.isSolid = True
	stone.tileID = 1
	stone.rRange = 5
	stone.gRange =5
	stone.bRange =5
	stone.translucency = .6
	tileManager["stone"] = stone


	stoneBackground = Tile(50,30,9)

	stoneBackground.isSolid = False
	stoneBackground.tileID = 0
	stoneBackground.rRange = 5
	stoneBackground.gRange = 5
	stoneBackground.bRange = 5
	stoneBackground.translucency = .97

	tileManager["stoneBackground"] = stoneBackground
