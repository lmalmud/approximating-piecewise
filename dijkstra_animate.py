## Creating a queue ##
'''
The below code creates a priority que. In aggregate, the priority que sorts the edges in a graph based on their length with two 
goals in mind. Adding another element requires linear time (is very fast) and crucially, the first item in the que is the item
with the lowest weight. In this case, the first item will be the next edge, and the weight represents the edge's length. Since 
this is not the main focus and there are dozens of queus with pros and cons, understanding the implementation of this binary 
heap queu will be left as an exercise to the reader. 
'''

from heapq import heapify, heappop, heappush
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random
 
class priority_queue():
    def __init__(self):
        self.queue = list()
        heapify(self.queue)
        self.index = dict()
    def push(self, priority, label):
        if label in self.index:
            self.queue = [(w,l) for w,l in self.queue if l != label]
                
            heapify(self.queue)
        heappush(self.queue, (priority, label))
        self.index[label] = priority
    
    def pop(self):
        if self.queue:
            return heappop(self.queue)
    
    def __contains__(self, label):
        return label in self.index
    
    def __len__(self):
        return len(self.queue)
  
## Implementing Dijkstra's Algorithm ##

'''
Dijkstra is not a recursive algorithm, because it only visits each vertex once. To run, it requires a weighted map of a graph as
well as a starting and ending vertex.
'''

def dijkstra_animate(weightmap, start, end, pts, ani_name="Approximation_Animation"):
    inf = float('inf')
    known = set()
    priority = priority_queue()

    fig, ax = plt.subplots()
    '''
    The way Dijkstra records paths is very clever. Rather than many lists of vertices, Dijkstra records the previous vertex 
    required to reach the next one. For example, it might record B:A and C:B, meaning the shortest route to C requires coming
    from B, and going to B requires coming from A.
    pts: array of the underlying vertex objects
    '''
    #The shortest route to the start is known to be from the start, since the distance from a point to itself is 0
    path = {start: start}

    artists = [] # will contain each frame in the animation
 
    #Each vertex is added to a que of vertices to visit with a weight, which represents how long it takes to reach.
    for vertex in weightmap:
        if vertex == start:
            #Since the algorithm starts on the first vertex, it takes no distance to reach.
            priority.push(0, vertex)
        else:
            #However, every other vertex has infinite weight, because the algorithm does not know if every vertex can be reached
            priority.push(inf, vertex)
    
    #Dijkstra keeps running until the last vertex it visited was the end
    last = start
    while last != end:
        
        #The first vertex in the priority que gives Dijkstra the vertex with the lowest total distance from the start. 
        (weight, current_vertex) = priority.pop()
        
        #Prevent the algorithm from retracing steps 
        if current_vertex not in known:
            #Dijkstra considers every vertex that can be reached from the current vertex
            for next_vertex in weightmap[current_vertex]:
                
                #The weight for a vertex in the que is the total distance Dijkstra has found to reach that vertex
                dist_upto_current = priority.index[current_vertex]
                    #Recall that each vertex begins at infinity
                
                #This calculates the total distance Dijkstra would have to travel to reach the next vertex from the current one
                dist_to_next = dist_upto_current + weightmap[current_vertex][next_vertex]
                    #The weightmap tells Dijkstra the distance from where it's standing to the next vertex
                    #dist_upto_current records how long it took Dijkstra to reach the current vertex
                    
                
                #This finds how long it took Dijkstra to reach the next vertex via another path
                dist_upto_next = priority.index[next_vertex]
                
                #If Dijkstra has found a shorter route to the next vertex, it does two things:
                if dist_to_next < dist_upto_next:
                    #It updates the total distance to reach the next vertex
                    priority.push(dist_to_next, next_vertex)
                        #As Dijkstra reaches more vertices, weights will be changed from infinity to a real number
                    
                    #It records how it reached that vertex
                    path[next_vertex] = current_vertex
            
            #Dijkstra then does all of the above for the vertex with the next lowest distance from the start
            last = current_vertex
            known.add(current_vertex)

            # want to draw all of the current shortest paths, which are stored in the "path" dictionary
            # for each vertex that has been discovered, we will draw a segment from that vertex to its predecessor
            this_frame = [] # using ArtistAnimation, we will build each frame of the animation one at a time
            # we will append every object that we wish to appear on this frame to this_frame objects

            # 1: Plot the original function
            points_x = [p.x for p in pts]
            points_y = [p.y for p in pts]
            
            p, = ax.plot(points_x, points_y, color="black", linestyle="dashed")
            this_frame.append(p)
            
            # Additionally, plot each vertex in the original function
            dot = ax.scatter(points_x, points_y, color='black')
            this_frame.append(dot)

            # 2: Draw all the options from the current vertex
            if current_vertex != end:
                # Color edges according to their length
                cmap = plt.get_cmap("Wistia")    
                adjacents = list(weightmap[current_vertex].keys())
                lengths = list(weightmap[current_vertex].values())
                max_length = max(lengths)
                if max_length == 0:
                    max_length = 0.001 # Avoid a divide by 0 error
                colors = [cmap(l / max_length) for l in lengths]

                # Draw each edge individually so color map works
                for i in range(len(lengths)):
                    line, = ax.plot((current_vertex.x, adjacents[i].x),(current_vertex.y, adjacents[i].y),
                                   color = colors[i])
                    # Label each edge with its length as well
                    text = ax.text((current_vertex.x + adjacents[i].x)/2, 
                                   (current_vertex.y + adjacents[i].y)/2, 
                                   f"{lengths[i]:.2f}", animated=True)
                    
                    this_frame.append(line)
                    this_frame.append(text)
                    
            

            # 3: color the current vertex as a red star
            current_dot, = ax.plot(current_vertex.x, current_vertex.y, '*', color='red')
            this_frame.append(current_dot)
            
            # Add the known vertices to the plot in orange
            known_x = [k.x for k in known]
            known_y = [k.y for k in known]
            known_dots = ax.scatter(known_x, known_y, color="orange")
            this_frame.append(known_dots)
            
            # Include this frame to the list of frames
            artists.append(this_frame)

    
    # Plot the final approximation at the end
    this_frame = []
    ending_path = reverse_path(path, start, end)
    for i in range(len(ending_path) - 1):
        p, = ax.plot((ending_path[i].x, ending_path[i+1].x), (ending_path[i].y, ending_path[i+1].y), 
                     color = "yellow", alpha=0.5)
        
        this_frame.append(p)
    x_coords = [v.x for v in ending_path]
    y_coords = [v.y for v in ending_path]
    dots = ax.scatter(x_coords, y_coords, marker="$\u263A$", s=100, color="orange")
                                        # Smiley face that's orange
    this_frame.append(dots)
    artists.append(this_frame)
    
    #Once Dijkstra has finished, it returns the distances from the start to each vertex it visited, and the path to get there
    ani = animation.ArtistAnimation(fig, artists, interval=200, repeat=True, blit=True)
    plt.show()
    
    # Save the animation as a gif that lasts 5 seconds
        # The animation wasn't working correctly before on my end
    writergif = animation.PillowWriter(fps=len(artists)//5) # Round to integer division
    ani.save(f'{ani_name}.gif', writer=writergif)
    return priority.index, path

## Making the Path Readable ##

'''
Since the Path is rather hard to follow for a human (Recall it is of the form B <- A, C <- D, F <- B, E <- A, is it clear what
the path from A to F is?), this function gives the specifc path from the start to the end by going backwards through the entire
path dictionary. 
'''

def reverse_path(path, start, end):
    progression = [end]
    while progression[-1] != start:
        progression.append(path[progression[-1]])
    return progression[::-1]
