class Edge:
    #The edge is built upon vertices, defined by a starting and ending vertex. Crucially, the edge also stores its own length
    def __init__(self, start, end, length=-1):
        self.start = start
        self.end = end
        self.length = length
        
    #Same as before, the below code allows the computer to represent the information in an edge in a useful way
    def __str__(self):
        return '{a} -> {b}'.format(a=self.start, b=self.end)
    
    def __repr__(self):
        return '{a} -> {b}'.format(a=self.start, b=self.end)