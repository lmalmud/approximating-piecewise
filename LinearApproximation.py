from Vertice import Vertice
from Edge import Edge
from Graph import Graph
from dijkstra import *
import matplotlib.pyplot as plt
from dijkstra_animate import *

'''
LinearApproximation.py
2025-04-28

Turns a set of points defining a piecewise function into a graph representation in order
to find a shortest path that will represent an optimal approximation to the piecewise
function, given specified cost parameters.
'''

class LinearApproximation:

    def __init__(self, points, alpha, beta, names=[]):
        '''
        Initializes a LinearApproximation object by constructing the corresponding graph.
        points: two-dimensional array of points: [[x1, y1], [x2, y2], ..., [xn, yn]]
        alpha: the additional incured cost of storage
        beta: the additional icured cost of error between true value and approximation
        names: names associated with each of the points
        '''
        if len(points) < 2:
            raise Exception("Must include at least two points in order to define a piecewise function")

        self.points = sorted(points) # Python automatically sorts multi-dimensional arrays by the first element
        self.alpha = alpha # The cost of storing a segment
        self.beta = beta # The cost of error

        if names == []:
            for i in range(len(points)):
                names.append(i)

        # Create a vertex for each point
        # Note that the points are sorted, so these vertices will also be in sorted order
        self.vertices = []
        for index, point in enumerate(self.points):
            self.vertices.append(Vertice(point[0], point[1], names[index]))

        self.edges = []
        # Insert an edge (i, j) for each i < j representing adding a segment between a_i, a_j
        for i, v_i in enumerate(self.vertices):
            for j, v_j in enumerate(self.vertices[i+1:]): # Only would insert an edge from vertices that come after
                cost = alpha
                for k in range(i, j+1):
                    # f_1(x_k): The true value of the function at x_k
                    f1_xk = self.f_1(self.points[k][0]) 
                    
                    # f_2(x_k): The value of the approximated function at x_k were there a segment between p_i and p_j
                    f2_xk = self.eval_segment(self.points[k][0], self.points[i], self.points[j])
                    cost += beta * pow(f1_xk - f2_xk, 2)
                self.edges.append(Edge(v_i, v_j, cost))

        self.graph = Graph(self.vertices, self.edges)
        self.s = self.vertices[0] # The source node must be the first point, corresponding to the first vertex
        self.t = self.vertices[-1] # The terminal node must be the last point, corresponding to the last vertex

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
        while before_point[0] < x and index < len(self.points):
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

        # Edge cases when a boundary point is the input
        if x == x1:
            return y1
        elif x == x2:
            return y2
        
        # Otherwise, calculate the point along the segment (x1, y1), (x2, y2)
        m = (y2-y1)/(x2-x1)
        return (m * (x - x1)) + y1

    def plt(self, fig, ax, pts=[], label=True):
        '''
        Plots the piecewise linear approximation described by the
        data contained in each Verticie object.
        fig: matplotlib figure
        ax: matplotlib axis
        pts: array of Vertices
        label: boolean (if true, points will be labeled)
        '''

        # If no parameter specified, plots the points that define the function
        if pts == []:
            pts = self.vertices

        # Plot a line for each segment between adjacent points
        for i in range(len(pts) - 1):
            plt.plot((pts[i].x, pts[i+1].x), (pts[i].y, pts[i+1].y), color = 'black')
        
        for i in range(len(pts)):
            plt.plot(pts[i].x, pts[i].y, 'o', color='black') # Add a dot at each point
            if label:
                ax.annotate(self.vertices[i].name, (pts[i].x, pts[i].y)) # Label the point with pi
    
    def plt_approximation(self, fig, ax, pts, label_original=False, label_approx=False):
        '''
        Plots both the original function and the approximated set of vertices on the same plot
        fig: matplotlib figure
        ax: matplotlib axis
        pts: array of Vertices used in the approximation
        '''
        self.plt(fig, ax, label=label_original) # Plot the original points and their labels

        # Plot a line for each segment between adjacent points in red for the segments chosen in the approximation
        for i in range(len(pts) - 1):
            plt.plot((pts[i].x, pts[i+1].x), (pts[i].y, pts[i+1].y), color = 'red')

        # Color each selected vertex to be red
        for i in range(len(pts)):
            plt.plot(pts[i].x, pts[i].y, 'o', color='red')
            if label_approx:
                ax.annotate(pts[i].name, (pts[i].x, pts[i].y), color='blue', weight='bold')


    def approximate(self):
        '''
        Runs Dijkstra's algorithm on the underlying graph in order to determine the new approximation.
        returns: array of the vertices chosen to be in the approximation
        '''

        # First item in result is node: shortest distance
        # Second item in result is node: predecessor in shortest path
        result = dijkstra(self.graph.WeightMap(), self.s, self.t)

        # Reverse path will determine the nodes that are traversed in the shortest path from p1 -> pn
        # These are the vertices that will define the optimal approximated piecewise function
        solution_vertices = reverse_path(result[1], self.s, self.t)

        return solution_vertices

    def animate_dijkstra(self):
        '''
        Runs the approximation algorithm and outputs the animated results as the algorithm progresses.
        ENtire animation and shortest path approximation conducted within dijkstra_animate.
        fig: matplotlib figure
        ax: matplotlib axis
        Returns: none
        '''
        dijkstra_animate(self.graph.WeightMap(), self.s, self.t, self.vertices)
