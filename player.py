from settings import *
import physics,rendering,pygame
class Player():
    def __init__(self,x,y) -> None:
        self.x = y
        self.y = x

        self.xspeed = 0
        self.yspeed = 0

        self.health = 20
        self.hunger = 20
        self.width = TILE_WIDTH * 1.4
        self.height = TILE_HEIGHT * 3

        self.onGround = False
        self.camera = rendering.Camera(self.x,self.y)
        self.collider = physics.Collider(x,y,self.width,self.height)
        self.collider.canClimb = True
        self.collider.hasGravity = True
        self.tool = None
        self.AI = None
        self.fly = False

        pass
    
    def applyPhysics(self,world):
        if callable(self.AI):
            self.AI(self)
            
        self.collider.x = self.x
        self.collider.y = self.y
        #print(self.xspeed,self.yspeed)
        self.collider.xSpeed = self.xspeed
        self.collider.ySpeed = self.yspeed
        #print(self.yspeed)
        #print(self.xspeed)
        self.collider.runPhysics(world)

        self.x = self.collider.x
        self.y = self.collider.y

        self.yspeed = self.collider.ySpeed
        self.xspeed = self.collider.xSpeed

        self.camera.x = self.x - (SCREEN_WIDTH/2 - self.width/2)
        self.camera.y = self.y - (SCREEN_HEIGHT/2 - self.height/2)
        self.onGround = self.collider.onGround

    def draw(self,surface):
        pygame.draw.rect(surface, (100,25,20), (SCREEN_WIDTH/2 - self.width/2,SCREEN_HEIGHT/2 - self.height/2,self.width,self.height))
        pass


    def showView(self,surface,buffers):
        
        self.camera.draw(surface,buffers)
        self.draw(surface)


    




