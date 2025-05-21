Taking inspiration from *Network Flows (Ahuja, Magnati, Orlin)*, we have implemented an approximation of a piecewise linear funciton by modeling the underlying graph as an undirected network.

A piecewise linear function is defined by the points at which the slope changes. For each of these points, we create a vertex and associate a weight between adjacent vertices to be the cost of storing that edge and the error that approximating that segment would induce.

Running a shortest path algorithm on the underlying network will then provide the optimal approximation based on the predefined weights for storage and approximation penalties.

We then applied such an approximation to two interesting examples: financial data and exploration of the cost parameters to approximate the sine funciton.
