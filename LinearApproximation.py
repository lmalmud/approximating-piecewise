from Verticie import Verticie
from Edge import Edge
from Graph import Graph

class LinearApproximation:

    def __init__(self, points, alpha, beta):
        self.points = points
        self.alpha = alpha # The cost of storing a segment
        self.beta = beta # The cost of error

        # Create a vertex for each point
        vertices = []
        for index, point in enumerate(points):
            vertices.append(Verticie(point[0], point[1], index))
        edges = []
        
        # Insert an edge (i, j) for each i < j representing adding a segment between a_i, a_j
        for i, v_i in enumerate(vertices):
            for j, v_j in enumerate(vertices):
                cost = alpha
                # FIXME: calculate the cost of this edge
                edges.append(Edge(v_i, v_j))
