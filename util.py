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

def sample_valves(index=0):
    return [[0,(3,0)],[0,(0,2)],[1,(4,0)],[1,(3,1)],[2,(2,1)],[2,(1,3)],[3,(0,3)],[3,(4,3)],[4,(3,3)],[4,(4,4)]]

def get_duration(start_time, message = None):
    return str((datetime.now() - start_time).total_seconds()*1000)+' ms'+(' - '+message or '')

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