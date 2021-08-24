class Matrix():
    def genMatrix(self,x,y):
        output = []
        for i in range(y):
            output.append([0]*x)
        return(output)

    def __init__(self,x,y) -> None:
        self.width = x
        self.height = y
        self.matrix = self.genMatrix(x,y)
        pass

    def __repr__(self) -> str:
        output = "\n"
        for y in self.matrix:
            output += str(y)+"\n"
        return(output)
        pass

    def __getitem__(self,loc):
        x,y = loc
        return(self.matrix[y][x])
    
    def __setitem__(self,loc,value):
        x,y = loc
        self.matrix[y][x] = value

    def convertTo(self,matrix,x,y):
        pass





class Vector3():
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z


    def __mul__(self,other):
        if type(other) == int or type(other) == float:
            return(Vector3(self.x*other,self.y*other,self.z*other))
        else:
            return(Vector3(self.x*other.x,self.y*other.y,self.z*other.z))
    

    def __add__(self,other):
        if type(other) == int or type(other) == float:
            return(Vector3(self.x+other,self.y+other,self.z+other))
        else:
            return(Vector3(self.x+other.x,self.y+other.y,self.z+other.z))
    

    def __sub__(self,other):
        if type(other) == int or type(other) == float:
            return(Vector3(self.x-other,self.y-other,self.z-other))
        else:
            return(Vector3(self.x-other.x,self.y-other.y,self.z-other.z))

    
    def __getitem__(self,loc):
        
        if loc == 0:
            return(self.x)
        elif loc == 1:
            return(self.y)
        else:
            return(self.z)
        
    
    def __setitem__(self,loc,value):
        if loc == 0:
            self.x = value
        elif loc == 1:
            self.y = value
        else:
            self.z = value

    def __repr__(self) -> str:
        return(f"{self.x},{self.y},{self.z}")
        pass



class Color():

    def __init__(self,r,g,b) -> None:
        self.r = r
        self.g = g
        self.b = b


    def __mul__(self,other):
        if type(other) == int or type(other) == float:
            return(Color(self.r*other,self.g*other,self.b*other))
        else:
            return(Color(self.r*other.r,self.g*other.g,self.b*other.b))
    

    def __truediv__(self,other):
        if type(other) == int or type(other) == float:
            return(Color(self.r/other,self.g/other,self.b/other))
        else:
            return(Color(self.r/other.r,self.g/other.g,self.b/other.b))
    

    def __add__(self,other):
        if type(other) == int or type(other) == float:
            return(Color(self.r+other,self.g+other,self.b+other))
        else:
            return(Color(self.r+other.r,self.g+other.g,self.b+other.b))
    

    def __sub__(self,other):
        if type(other) == int or type(other) == float:
            return(Color(self.r-other,self.g-other,self.b-other))
        else:
            return(Color(self.r-other.r,self.g-other.g,self.b-other.b))

    
    def __getitem__(self,loc):
        
        if loc == 0:
            return(self.r)
        elif loc == 1:
            return(self.g)
        else:
            return(self.b)
        
    
    def __setitem__(self,loc,value):
        if loc == 0:
            self.r = value
        elif loc == 1:
            self.g = value
        else:
            self.b = value

    def __repr__(self) -> str:
        return(f"{self.r},{self.g},{self.b}")
        pass


        
    

def sign(x):
    if x < 0:
        return(-1)
    if x > 0:
        return(1)
    return(0)

test = Matrix(4,4)
test[1,2] = 4
print(test)
print(test[1,2])












