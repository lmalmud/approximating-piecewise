from Verticie import Verticie
from Edge import Edge
from Graph import Graph
from dijkstra import *

class LinearApproximation:

    def __init__(self, points, alpha, beta):
        '''
        Initializes a LinearApproximation object by constructing the corresponding graph.
        points: two-dimensional array of points: [[x1, y1], [x2, y2], ..., [xn, yn]]
        alpha: the additional incured cost of storage
        beta: the additional icured cost of error between true value and approximation
        '''

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

    def plt(self, pts):
        '''
        Plots the piecewise linear approximation described by the
        data contained in each Verticie object.
        pts: array of Verticie objects
        '''
        pass

    def approximate(self):
        '''
        Runs Dijkstra's algorithm on the underlying graph in order to determine the new approximation.
        returns: array of Verticie objects representing the points chosen to be in the approximation
        '''
        pass

    def animate_dijkstra(self, pts_approx):
        '''
        Plots the points describing the original function and draws line segments between
        each consecutive pair of points in pts_approx.
        pts_approx: array of Verticie objects
        '''
        pass
