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
    if not item.outOfRange:
       blockX,blockY = world.getBlock(x,y)
       tile = item.places
    
       if world[blockX,blockY].tile.tileName != tile and not world[blockX,blockY].tile.isSolid:
           world[blockX,blockY].tile = tileManager[tile]
           buffers.updateTile(blockX,blockY)
           world.updateLighting(blockX,blockY,tileManager[tile])
           item.count -= 1




def addContent():

	





	block = Tool("block")
	block.leftAction = placeBlock
	block.icon = pygame.image.load("contentPacks/basegame/assets/none.bmp")
	block.places = None
	block.maxRange = 6
	block.stackable = True
	#print(itemManager.items)
	itemManager["block"] = block
	





	air = Tile(0,0,220)
	air.isSolid = False
	air.bRange = 5
	air.sunlight = 1
	air.translucency = .1
	air.rRange = 0
	air.bRange = 0
	air.gRange = 0
	air.image = pygame.image.load("contentPacks/basegame/assets/air.bmp")
	#air.darkenImage()
	
	
	
	
	
	tileManager["air"] = air


	dirt = Tile(117 , 76 ,19)
	dirt.isSolid = True
	dirt.tileID = 1
	dirt.rRange = 5
	dirt.bRange = 5
	dirt.translucency = .7
	dirt.image = pygame.image.load("contentPacks/basegame/assets/dirt.bmp")
	dirt.drops = "dirt"
	
	
	dirtItem = itemManager["block"] #take generic block
	dirtItem.places = "dirt" #configure it for dirt
	dirtItem.icon = pygame.transform.scale(pygame.image.load("contentPacks/basegame/assets/dirt.bmp"), (20, 20))
	itemManager["dirt"] = dirtItem #add new item back
	
	
	
	#dirt.darkenImage()
	tileManager["dirt"] = dirt


	dirtBackground = Tile(50,30,9)
	dirtBackground.isSolid = False
	dirtBackground.tileID = 0
	dirtBackground.rRange = 5
	dirtBackground.bRange = 5
	dirtBackground.translucency = .85

	dirtBackground.image = pygame.image.load("contentPacks/basegame/assets/dirtbackground.bmp")
	#dirtBackground.darkenImage()
	tileManager["dirtBackground"] = dirtBackground


	stone = Tile(70,70,80)
	stone.isSolid = True
	stone.tileID = 1
	stone.rRange = 5
	stone.gRange =5
	stone.bRange =5
	stone.translucency = .9
	tileManager["stone"] = stone


	stoneBackground = Tile(50,30,9)
	stoneBackground.isSolid = False
	stoneBackground.tileID = 0
	stoneBackground.rRange = 5
	stoneBackground.gRange = 5
	stoneBackground.bRange = 5
	stoneBackground.translucency = .94

	tileManager["stoneBackground"] = stoneBackground
	
	
	
	
	
	
	
	
	
	
	
	bedrock = Tile(50,30,9)
	
	bedrock.isSolid = True
	bedrock.tileID = 0
	bedrock.rRange = 5
	bedrock.gRange = 5
	bedrock.bRange = 5
	bedrock.translucency = .9
	bedrock.unbreakable = True
	bedrock.image = pygame.image.load("contentPacks/basegame/assets/bedrock.bmp")
	tileManager["bedrock"] = bedrock
	
	
	itemManager.addFromTile(bedrock,"contentPacks/basegame/assets/bedrock.bmp")
	
	
	
	
	
	
	
	iron = Tile(117 , 76 ,19)
	iron.isSolid = True
	iron.tileID = 1
	iron.rRange = 5
	iron.bRange = 5
	iron.translucency = .6
	iron.image = pygame.image.load("contentPacks/basegame/assets/iron.bmp")
	tileManager["iron"] = iron
	
	itemManager.addFromTile(iron,"contentPacks/basegame/assets/iron.bmp")
	
	
	
	
	
	
	
	
	
	
	
	torchTile = Tile(100, 183, 0) #create a new tile
	torchTile.emissionlevel = 2 #have that tile emit light at a level of 1
	torchTile.isSolid = False
	torchTile.translucency = 1 #have light pass through the tile perfectly
	torchTile.image = pygame.image.load("contentPacks/basegame/assets/torch.bmp")
	
	tileManager["torch"] = torchTile #tell the game about this new tile
	itemManager.addFromTile(torchTile,"contentPacks/basegame/assets/torch.bmp")
	
	
	#dirtItem = itemManager["iron"] #take generic block
	#dirtItem.places = "iron" #configure it for dirt
	#dirtItem.icon = pygame.transform.scale(pygame.image.load("contentPacks/basegame/assets/iron.bmp"), (20, 20))
	#itemManager["dirt"] = dirtItem #add new item back
	
	
	
	
	
	
	#bedrockItem = itemManager["block"] #take generic block
	#bedrockItem.places = "bedrock" #configure it for dirt
	#bedrockItem.icon = pygame.transform.scale(pygame.image.load("contentPacks/basegame/assets/bedrock.bmp"), (20, 20))
	#itemManager["bedrock"] = bedrockItem #add new item back
	
	
	
	
	
	
	
	
	
	
	
	
