## Creating a queue ##
'''
The below code creates a priority que. In aggregate, the priority que sorts the edges in a graph based on their length with two 
goals in mind. Adding another element requires linear time (is very fast) and crucially, the first item in the que is the item
with the lowest weight. In this case, the first item will be the next edge, and the weight represents the edge's length. Since 
this is not the main focus and there are dozens of queus with pros and cons, understanding the implementation of this binary 
heap queu will be left as an exercise to the reader. 
'''

from heapq import heapify, heappop, heappush
 
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

def dijkstra(weightmap, start, end):
    inf = float('inf')
    known = set()
    priority = priority_queue()
    '''
    The way Dijkstra records paths is very clever. Rather than many lists of vertices, Dijkstra records the previous vertex 
    required to reach the next one. For example, it might record B:A and C:B, meaning the shortest route to C requires coming
    from B, and going to B requires coming from A.
    '''
    #The shortest route to the start is known to be from the start, since the distance from a point to itself is 0
    path = {start: start}
 
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
    
    #Once Dijkstra has finished, it returns the distances from the start to each vertex it visited, and the path to get there
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
