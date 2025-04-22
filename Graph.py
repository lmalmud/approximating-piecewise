class Graph:
    #A graph is a collection of vertices and edges, which are both stored as a list.
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
    
    '''
    This is the most important part of the Graph, the Map. It is a dictionary, meaning that each value (a vertex) points to 
    some other piece of information. Basically, if the computer is asked what vertices connect to a starting vertex, it can open 
    the Map dictionary and return the list associated with the starting vertice.
    '''
    def Map(self):
        return {v:[e.end for e in self.edges if e.start == v] for v in self.vertices}
    
    #The WeightMap, in addition to tracking which vertices are connected, assigns a weight to this connection. 
    def WeightMap(self):
        return {v: {e.end: e.length for e in self.edges if e.start == v} for v in self.vertices}
        '''
        Here, the weight is just the distance between two vertices, but this can be changed or updated depending on
        what the weight is supposed to represent. For example, when representing roads, the weight between two vertices might
        be lowered if the edge connecting them has low traffic. 
        '''