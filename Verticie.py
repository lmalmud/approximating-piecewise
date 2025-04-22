class Vertice:
    #The important information a vertice should have is position data (x and y cartesian coordinates) and a name 
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    #The below code allows the computer to know how it should represent and interpret the information in a vertice when asked
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return str(self.name)
    
    def __gt__(self, vertex):
        if self.x > vertex.x:
            return True
        else:
            return False
        
    def __lt__(self, vertex):
        if self.x < vertex.x:
            return True
        else:
            return False