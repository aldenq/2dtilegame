import copy
class ItemManager():
    def __init__(self) -> None:
        self.items= {}
        pass


    def __getitem__(self,loc):
        return(copy.copy(self.items[loc]))
    
    def addTool(self,loc,value):
        self.items[loc] = value

    def __setitem__(self,loc,value):
        self.items[loc]=value











class Tool():
    def __init__(self,name) -> None:
        self.leftAction  = None
        self.rightAction = None
        self.durability = 0
        self.count = 0
        self.stackable = False
        self.name = name
        pass
    
    def leftClick(self, mouseX,mouseY):
        if callable(self.leftAction):
            self.leftAction(self,mouseX,mouseY)
    
    def rightClick(self,mouseX,mouseY):
        if callable(self.rightAction):
            self.rightAction(self,mouseX,mouseY)
    

    

    