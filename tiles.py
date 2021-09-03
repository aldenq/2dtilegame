import copy
import random,pygame
from settings import MAX_DARK
from helpers import *
class Tile():
    def __init__(self,r,g,b) -> None:
        self.color = Color(r,g,b)

        self.rRange = 0
        self.gRange = 0
        self.bRange = 0
        self.tileID = 0
        self.tileName =0
        self.isSolid = False
        self.lightLevel = 0
        self.sunlight = 0
        self.emissionlevel = 0

        self.sunlightEmissive = 0
        self.translucency = .4
        self.colorTranslucency = None
        self.image = None
        self.onSpawn = None 
        self.lightSources = None
        self.drops = None
        self.unbreakable = False
        pass
    def darkenImage(self):
        dark = pygame.Surface(self.image.get_size())
        dark.set_alpha(MAX_DARK)
        dark.fill((0, 0, 0))
        self.image.blit(dark, (0, 0))

    def __repr__(self) -> str:
        return(str(self.tileID))

class TileManager():

    def __init__(self) -> None:
        self.tiles = {}

        self.lastTile = None
        lastTileName = None
        pass
    

    def fastCopy(self,loc):
        

        tile = (self.tiles[loc])
        retTile = Tile(tile.color.r,tile.color.g,tile.color.b  )


        retTile.image = tile.image
        retTile.tileName = tile.tileName
        retTile.isSolid = tile.isSolid
        retTile.sunlight = tile.sunlight
        retTile.emissionlevel = tile.emissionlevel
        retTile.translucency = tile.translucency
        retTile.drops = tile.drops
        retTile.unbreakable = tile.unbreakable
        retTile.sunlightEmissive = tile.sunlightEmissive
        retTile.updates = 0
        
        retTile.colorTranslucencyR = (1 - retTile.color.r/255)*(1-retTile.translucency)
        retTile.colorTranslucencyG = (1 - retTile.color.g/255)*(1-retTile.translucency)
        retTile.colorTranslucencyB = (1 - retTile.color.b/255)*(1-retTile.translucency)
        return(retTile)

    def __getitem__(self,loc):
        #print(loc,"getting tile")
        retTile = copy.copy(self.tiles[loc])
        retTile.color = copy.copy(retTile.color)

        if callable(retTile.onSpawn):
            retTile.onSpawn(retTile)



        retTile.color.r += random.randint(-retTile.rRange,retTile.rRange )
        retTile.color.g += random.randint(-retTile.gRange,retTile.gRange )
        retTile.color.b += random.randint(-retTile.bRange,retTile.bRange )

        #retTile.colorTranslucency = (retTile.color/255)*(1-retTile.translucency)
        retTile.colorTranslucency = Color(0,0,0)
        retTile.colorTranslucency.r = (1 - retTile.color.r/255)*(1-retTile.translucency)
        retTile.colorTranslucency.g = (1 - retTile.color.g/255)*(1-retTile.translucency)
        retTile.colorTranslucency.b = (1 - retTile.color.b/255)*(1-retTile.translucency)
        #print(retTile.colorTranslucency, retTile.tileName)
        return(retTile)
    
    def __setitem__(self,name,tile):
        tile.tileName = name
        self.tiles[name] = tile
    

    def addTile(self,name,tile):
        self.tiles[name] = tile
        tile.tileName = name
        tile.image = pygame.Surface.convert(tile.image)











    

    