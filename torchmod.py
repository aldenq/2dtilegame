
from player import Player
import main
import pygame

from entities import Entity
from tools import Tool
import time
import tiles


torchTile = tiles.Tile(100, 183, 0) #create a new tile
torchTile.emissionlevel = .5 #have that tile emit light at a level of 1
torchTile.isSolid = False
torchTile.translucency = 1 #have light pass through the tile perfectly
tiles.tileManager["torch"] = torchTile #tell the game about this new tile

def placeTorch(item,x,y):
    blockX,blockY = main.world.getBlock(x,y) 
    if main.world[blockX,blockY].tile.tileName != "torch": #only place the block if the block selected is not already a torch
        main.setblock(blockX,blockY,tiles.tileManager["torch"])
    pass

def mineBlock(item,x,y):
    blockX,blockY = main.world.getBlock(x,y)
    if main.world[blockX,blockY].tile.tileName != "stone":
        main.setblock(blockX,blockY,tiles.tileManager["stone"])
    pass


torch = Tool("torch")
torch.leftAction = placeTorch
torch.rightAction = mineBlock
main.mainPlayer.tool = torch #equip the player with this new tool


main.startGame()









