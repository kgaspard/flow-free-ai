# Attribution Information: Some classes used in this file (PriorityQueue, Counter) were developed at UC Berkeley.
# Thank you to Dan Klein (klein@cs.berkeley.edu) and Pieter Abbeel (pabbeel@cs.berkeley.edu) for making them 
# publicly available through https://ai.berkeley.edu

import random, heapq
from datetime import datetime
import numpy as np

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

def tupleDiff(tuple1,tuple2):
    return tuple(map(lambda i, j: i - j, tuple1, tuple2))

def manhattanDistance(tuple1,tuple2):
    return abs(tuple1[0] - tuple2[0]) + abs(tuple1[1] - tuple2[1])

def pickRandomElement(input_list):
    return random.choice(input_list)

def flipCoin( p ):
    r = random.random()
    return r < p

def crossProductDirection(tuple1,tuple2):
    a = np.array([tuple1[0],tuple1[1],0])
    b = np.array([tuple2[0],tuple2[1],0])
    direction = 'None'
    if np.cross(a,b)[2] < 0: direction='Left'
    elif np.cross(a,b)[2] > 0: direction='Right'
    return direction

def getSmallerVector(tuple1,tuple2):
    if abs(tuple1[0])+abs(tuple1[1]) > abs(tuple2[0])+abs(tuple2[1]): return tuple2
    else: return tuple1

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

class Counter(dict):

    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        for key in keys:
            self[key] += count

    def argMax(self):
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        return sum(self.values())

    def normalize(self):
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

class Search:
    def  __init__(self):
        pass

    def graphSearch(self, start_state, goal_state_checker_function, next_states_function, cost_function, priority_queue=None, return_priority_queue=False, all_solutions=False, track_visited=False, **kwargs):
        priority_queue = priority_queue or PriorityQueue()
        if not priority_queue.items(): priority_queue.push((start_state,[start_state],0),0)
        heuristic = kwargs.get('heuristic', None)
        solution_paths = []
        if track_visited: visited=[start_state]

        while not priority_queue.isEmpty():
            state, path, total_cost = priority_queue.pop()
            if goal_state_checker_function(state):
                if all_solutions:
                    solution_paths.append(path)
                else:
                    if return_priority_queue:
                        return [path],priority_queue
                    else:
                        return state if track_visited else [path]
            next_states = next_states_function(state) if track_visited else next_states_function(path)
            for new_state in next_states:
                cost = 1
                if ((not track_visited) and (new_state not in path)) or (track_visited and (new_state not in visited)):
                    cost = cost_function(total_cost,cost)
                    heuristic_value = heuristic(new_state) if heuristic else 0
                    priority_queue.push((new_state,path+[new_state],cost),cost + heuristic_value)
                    if track_visited: visited.append(new_state)
        if return_priority_queue:
            return solution_paths,priority_queue
        else:
            return solution_paths
    
    def breadthFirstSearch(self,start_state,goal_state_checker_function,next_states_function,**kwargs):
        cost_function = lambda x,y : x+1
        return self.graphSearch(start_state=start_state,goal_state_checker_function=goal_state_checker_function, next_states_function=next_states_function, cost_function=cost_function, **kwargs)

    def depthFirstSearch(self,start_state,goal_state_checker_function,next_states_function, **kwargs):
        fn = lambda x,y : x-1
        return self.graphSearch(start_state=start_state,goal_state_checker_function=goal_state_checker_function, next_states_function=next_states_function, cost_function=fn, **kwargs)

    def aStarSearch(self,start_state,goal_state,next_states_function, **kwargs):
        cost_function = lambda x,y : x+y
        heuristic = lambda state: manhattanDistance(state.pos,goal_state.pos)
        goal_state_checker_function = lambda state : state == goal_state
        return self.graphSearch(start_state=start_state,goal_state_checker_function=goal_state_checker_function, next_states_function=next_states_function, cost_function=cost_function, heuristic=heuristic, **kwargs)