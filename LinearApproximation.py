from Vertice import Vertice
from Edge import Edge
from Graph import Graph
from dijkstra import *
import matplotlib.pyplot as plt

class LinearApproximation:

    def __init__(self, points, alpha, beta):
        '''
        Initializes a LinearApproximation object by constructing the corresponding graph.
        points: two-dimensional array of points: [[x1, y1], [x2, y2], ..., [xn, yn]]
        alpha: the additional incured cost of storage
        beta: the additional icured cost of error between true value and approximation
        '''

        if len(points) < 2:
            raise Exception("Must include at least two points in order to define a piecewise function")

        self.points = sorted(points) # Python automatically sorts multi-dimensional arrays by the first element
        self.alpha = alpha # The cost of storing a segment
        self.beta = beta # The cost of error

        # Create a vertex for each point
        vertices = []
        for index, point in enumerate(points):
            vertices.append(Vertice(point[0], point[1], index))

        edges = []
        # Insert an edge (i, j) for each i < j representing adding a segment between a_i, a_j
        for i, v_i in enumerate(vertices):
            for j, v_j in enumerate(vertices):
                cost = alpha
                # FIXME: calculate the cost of this edge
                edges.append(Edge(v_i, v_j))

    def f_1(self, x):
        ''' Evalutes f_1(x), where f_1 is the true function
        defined by the points
        x: real number
        Returns: real number'''

        # Ensure that point we wish to evaluate the funciton at is within the domain
        if x < self.points[0][0]: # Below the lowest point
            raise Exception(f'x-coordinate too small: must be within the function domain of: [{self.points[0][0]}, {self.points[-1][0]}]')
        if x > self.points[-1][0]: # Above the largest point
            raise Exception(f'x-coordinate too large: must be within the function domain of: [{self.points[0][0]}, {self.points[-1][0]}]')
        
        index = 0
        before_point = self.points[index]
        while before_point[0] < x:
            index += 1
            before_point = self.points[index]
        after_point = self.points[-1]
        if index < len(self.points) - 1: # The point is not the last point
            after_point = self.points[index+1]
        else: # In this case, x is the last point, so use the last segment
            before_point = self.points[index-1]

        # To debug the boundaries:
        # print(f'x: {x}, before_point: {before_point}, after_point: {after_point}')

        # The main amount of work in this function is to determine the approproate
        # points that define the segment that x is located in.
        return self.eval_segment(x, before_point, after_point)

    def eval_segment(self, x, pt1, pt2):
        ''' Returns the value of the linear function defined by the line through
        p1 and p2
        x: real number
        pt1:[x1, y1]
        pt2: [x2, y2]
        f(x) = (y2-y1)/(x2-x1)(x - x1) + y1
        Returns: real number
        '''
        x1 = pt1[0]
        y1 = pt1[1]
        x2 = pt2[0]
        y2 = pt2[1]
        m = (y2-y1)/(x2-x1)
        return (m * (x - x1)) + y1

    def plt(self, pts=[]):
        '''
        Plots the piecewise linear approximation described by the
        data contained in each Verticie object.
        pts: array of points: [[x1, y1], ..., [xn, yn]]
        '''

        fig, ax = plt.subplots()
        # If no parameter specified, plots the points that define the function
        if pts == []:
            pts = self.points

        # Plot a line for each segment between adjacent points
        for i in range(len(pts) - 1):
            plt.plot((pts[i][0], pts[i+1][0]), (pts[i][1], pts[i+1][1]), color = 'black')
        
        for i in range(len(pts)):
            plt.plot(pts[i][0], pts[i][1], 'o', color='black') # Add a dot at each point
            ax.annotate(f'p{i}', (pts[i][0], pts[i][1])) # Label the point with pi

        plt.show()

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
