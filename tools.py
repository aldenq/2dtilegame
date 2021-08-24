class Tool():
    def __init__(self,name) -> None:
        self.leftAction  = None
        self.rightAction = None
        self.durability = 0
        pass
    
    def leftClick(self, mouseX,mouseY):
        if callable(self.leftAction):
            self.leftAction(self,mouseX,mouseY)
    
    def rightClick(self,mouseX,mouseY):
        if callable(self.rightAction):
            self.rightAction(self,mouseX,mouseY)
    

    

    