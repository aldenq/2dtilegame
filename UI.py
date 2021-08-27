from settings import *
from helpers import *
import pygame
class HotBar():
    def __init__(self) -> None:
        self.width = SCREEN_WIDTH
        self.height = ICON_HEIGHT + 10


    def draw(self,player,surface):
        pygame.draw.rect(surface,(0,0,0),(0,0,self.width,self.height))
        

        for i in range(INVENTORY_WIDTH):
            item = player.inventory[i,0]
            if i == player.hotbarSelect:
                pygame.draw.rect(surface, (80,80,80), (i*(ICON_WIDTH+5)-5,0,30,30))
            if item:
                item.drawIcon(surface,i*(ICON_WIDTH+5),5)
        
        #
        pass