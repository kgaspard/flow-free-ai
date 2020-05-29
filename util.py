import random, heapq
from datetime import datetime

def random_color():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)

def color_array(num_of_colors):
    palette = ['#0AFFAB','#2509EB','#FF3D37','#EBBA28','#2BFF33','#BDECFF','#4226EB','#FF57FA','#EB350C','#FFD791']
    colors = []
    for i in range(num_of_colors):
        if i<len(palette):
            colors.append(palette[i])
        else:
            colors.append(random_color())
    return colors

def checkAdjacency(tuple1,tuple2):
    if tuple1[0] == tuple2[0] and abs(tuple1[1] - tuple2[1]) <= 1: return True
    elif tuple1[1] == tuple2[1] and abs(tuple1[0] - tuple2[0]) <= 1: return True
    else: return False

def get_duration(start_time, message = None):
    return str((datetime.now() - start_time).total_seconds()*1000)+' ms'+(' - '+message or '')

def tupleSwap(tuple):
    return (tuple[1],tuple[0])

def tupleAdd(tuple1,tuple2):
    return tuple(map(lambda i, j: i + j, tuple1, tuple2))

def tupleScale(tuple1,scalar):
    return tuple(map(lambda i: i * scalar, tuple1))

def manhattanDistance(tuple1,tuple2):
    return abs(tuple1[0] - tuple2[0]) + abs(tuple1[1] - tuple2[1])

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
    
    def items(self):
        return list(item for _, _, item in self.heap)

class Search:
    def  __init__(self):
        pass

    def graphSearch(self, start_state, goal_state, next_states_function, cost_function, priority_queue=None, return_priority_queue=False, all_solutions=False, **kwargs):
        priority_queue = priority_queue or PriorityQueue()
        if not priority_queue.items(): priority_queue.push((start_state,[start_state],0),0)
        visited = []   # need to use list for Python as can't have nested sets. Ok as anyway checking if exists before inserting
        first_pop = True
        heuristic = kwargs.get('heuristic', None)
        solution_paths = []

        while not priority_queue.isEmpty():
            state, path, total_cost = priority_queue.pop()
            # print(path,priority_queue.items())
            if first_pop:
                visited = path
                first_pop = False
            if state == goal_state:
                if all_solutions:
                    solution_paths.append(path)
                else:
                    if return_priority_queue:
                        return [path],priority_queue
                    else:
                        return [path]
            for new_state in next_states_function(path):
                cost = 1
                if new_state not in path:
                    cost = cost_function(total_cost,cost)
                    heuristic_value = heuristic(new_state) if heuristic else 0
                    priority_queue.push((new_state,path+[new_state],cost),cost + heuristic_value)
                    if not all_solutions: visited.append(new_state)
        if return_priority_queue:
            return solution_paths,priority_queue
        else:
            return solution_paths
    
    def breadthFirstSearch(self,start_state,goal_state,next_states_function,**kwargs):
        cost_function = lambda x,y : x+1
        return self.graphSearch(start_state=start_state,goal_state=goal_state, next_states_function=next_states_function, cost_function=cost_function, **kwargs)

    def depthFirstSearch(self,start_state,goal_state,next_states_function, **kwargs):
        fn = lambda x,y : x-1
        return self.graphSearch(start_state=start_state,goal_state=goal_state, next_states_function=next_states_function, cost_function=fn, **kwargs)

    def aStarSearch(self,start_state,goal_state,next_states_function, **kwargs):
        cost_function = lambda x,y : x+y
        heuristic = lambda state: manhattanDistance(state.pos,goal_state.pos)
        return self.graphSearch(start_state=start_state,goal_state=goal_state, next_states_function=next_states_function, cost_function=cost_function, heuristic=heuristic, **kwargs)