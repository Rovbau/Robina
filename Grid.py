import heapq
import pickle


class SquareGrid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):
        return id not in self.walls
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super(GridWithWeights,self).__init__(width, height)
        self.weights = {}
    
    def cost(self, a, b):
        return self.weights.get(b, 1)

    def obstaclesInGrid(self, obstacles):
        """GlobaleHinderniss (x[cm],y[cm]) in Grid eintragen (RasterX,RasterY)"""        
        unpaintedObstacles=obstacles

        for obstacle in unpaintedObstacles:
            obstacle_x_grid=int(obstacle[0]/10)
            obstacle_y_grid=int(obstacle[1]/10)
            
            if (obstacle_x_grid,obstacle_y_grid) not in  self.walls:
                self.walls.append((obstacle_x_grid,obstacle_y_grid))

        #Hindernisse speichern            
        pickelObstacles=open( "RoboObstacles.p", "wb" )
        pickle.dump(self.walls,pickelObstacles)
	pickelObstacles.close()
        
        return(self.walls)
            
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        #print(current)
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = "\u2192"
        if x2 == x1 - 1: r = "\u2190"
        if y2 == y1 + 1: r = "\u2193"
        if y2 == y1 - 1: r = "\u2191"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#" * width
    return r

def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width))  #end=""
        print()

if __name__ == "__main__":

    start=(2,2)
    goal=(7,7)
    
    g = GridWithWeights(10, 10)
    g.walls = g.obstaclesInGrid([(0, 50),(10, 50),(20, 50),(30, 50),(40, 50),(90, 90)])

    came_from, cost_so_far = a_star_search(g, start, goal)

    path=reconstruct_path(came_from, start, goal)
    print(path)
    draw_grid(g, width=1, point_to=came_from, start=start,goal=goal)




        
        
