import copy,pygame
import pygame.freetype

from settings import ICON_HEIGHT, ICON_WIDTH

countFont = pygame.freetype.SysFont('Comic Sans MS', 15)

class ItemManager():
    def __init__(self) -> None:
        self.items= {}
        self.standardActions = None
        pass


    def __getitem__(self,loc):
        return(copy.copy(self.items[loc]))
    
    def addTool(self,loc,value):
        self.items[loc] = value

    def __setitem__(self,loc,value):
        self.items[loc]=value
    

    def addFromTile(self,tile,imagePath):
        tool = Tool(tile.tileName)
        tool.icon = pygame.transform.scale(pygame.image.load(imagePath), (ICON_WIDTH,ICON_HEIGHT))
        tool.places = tile.tileName
        tool.stackable = True
        tool.leftAction = self.standardActions.placeBlock
        tile.drops = tile.tileName 
        self.items[tile.tileName] = tool
        return(tool)











class Tool():
    
    def __init__(self,name) -> None:
        self.leftAction  = None
        self.rightAction = None
        self.durability = 0
        self.count = 1
        self.stackable = False
        self.name = name
        self.icon = None
        self.user = None
        self.maxRange = 0
        self.outOfRange = False
        pass
    
    def leftClick(self, mouseX,mouseY):
        if callable(self.leftAction):
            self.leftAction(self,mouseX,mouseY)
    
    def rightClick(self,mouseX,mouseY):
        if callable(self.rightAction):
            self.rightAction(self,mouseX,mouseY)

    

    def drawIcon(self,surface,x,y):
        textsurface,rect = countFont.render(str(self.count), fgcolor = (255, 255, 255),bgcolor=None)
        #print(textsurface)
        self.icon.set_alpha(255)
        surface.blit(self.icon,(x,y))


        surface.blit(textsurface,(x + ICON_WIDTH/2,y + ICON_HEIGHT - 6))

   
        

    

    

    