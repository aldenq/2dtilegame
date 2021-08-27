class Actions:
    """
    general way of packaging up a bunch of common high level actions so they can be easily ran by distant files
    this actions are especially ones that are likely to be ran by content packs
    
    """
    def __init__(self, world, buffers, mainPlayer,tileManager,itemManager,entityManager):
        self.world= world
        self.buffers=buffers
        self.mainPlayer=mainPlayer

        self.tileManager = tileManager
        self.itemManager = itemManager
        self.entityManager = entityManager

        tileManager.Actions = self



    def placeBlock(self,item,x,y):
        if not item.outOfRange:
            blockX,blockY = self.world.getBlock(x,y)
            tile = item.places
            
            if self.world[blockX,blockY].tile.tileName != tile and not self.world[blockX,blockY].tile.isSolid:
                self.world[blockX,blockY].tile = self.tileManager[tile]
                self.buffers.updateTile(blockX,blockY)
                self.world.updateLighting(blockX,blockY,self.tileManager[tile])
                item.count -= 1