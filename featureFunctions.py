import util

class Turn:
  def __init__(self,pos = (0,0), direction = 'None'):
      self.pos = pos
      self.direction = direction
  
  def __repr__(self):
      return '('+str(self.pos)+', '+str(self.direction)+')'

  def __eq__(self,other):
      return self.pos == other.pos and self.direction == other.direction

class Box:
  def __init__(self,corners = ((0,0),(0,0),(0,0),(0,0)), value = 0):
      self.corners = corners

  def getRectangleBounds(self):
    side1 = util.tupleDiff(self.corners[0],self.corners[1])
    side2 = util.tupleDiff(self.corners[3],self.corners[2])
    new_side = util.getSmallerVector(side1,side2)
    new_corners=[util.tupleAdd(self.corners[1],new_side),self.corners[1],self.corners[2],util.tupleAdd(self.corners[2],new_side)]
    x_coords = [corner[0] for corner in new_corners]
    y_coords = [corner[1] for corner in new_corners]
    return ((min(x_coords),max(x_coords)),(min(y_coords),max(y_coords)))

  def pointsInBoxRectangle(self,points):
    rectangle_bounds = self.getRectangleBounds()
    points_in_rectangle = []
    for point in points:
      if point[0] >= rectangle_bounds[0][0] and point[0] <= rectangle_bounds[0][1] and point[1] >= rectangle_bounds[1][0] and point[1] <= rectangle_bounds[1][1]:
        points_in_rectangle.append(point)
    return points_in_rectangle

  
  def __repr__(self):
      return self.corners.__repr__()
      # return '('+corners.__repr__()+', '+str(value)+')'

  def __eq__(self,other):
      return self.corners == other.corners
      # and self.value == other.value

def number_of_turns_in_path(path):
  n = len(path)
  turns = 0
  if n <= 2: return turns
  for i in range(n-2):
    if util.tupleDiff(path[i+2],path[i+1]) != util.tupleDiff(path[i+1],path[i]): turns += 1
  return turns

def turns_array(path):
  n = len(path)
  turns = []
  if n >= 1: turns.append(Turn(pos=path[0],direction='Start'))
  if n>2:
    for i in range(n-2):
      segment_after = util.tupleDiff(path[i+2],path[i+1])
      segment_before = util.tupleDiff(path[i+1],path[i])
      if segment_after != segment_before:
        turns.append(Turn(pos=path[i+1],direction=util.crossProductDirection(segment_before,segment_after)))
  if n>=2: turns.append(Turn(pos=path[-1],direction='End'))
  return turns

def boxes_in_path(path):
  turns = turns_array(path)
  boxes=[]
  direction = '-'
  for i in range(len(turns)):
    turn = turns[i]
    if i>0 and turn.direction == turns[i-1].direction:
      boxes.append(Box(corners=(turns[i-2].pos,turns[i-1].pos,turn.pos,turns[i+1].pos)))
  return boxes

### If we want to track boxes as we go along:
# def boxes_in_path(path):
#   n = len(path)
#   turns = []
#   if n >= 1: turns.append((path[0],'Start'))
#   if n>2:
#     direction='-'
#     box_counter = 0
#     for i in range(n-2):
#       if util.tupleDiff(path[i+2],path[i+1]) != util.tupleDiff(path[i+1],path[i]):
#         new_direction = util.crossProductDirection(util.tupleDiff(path[i+1],path[i]),util.tupleDiff(path[i+2],path[i+1]))
#         turns.append((path[i+1],new_direction))
#         # 2 left turns or 2 right turns is a box
#         if new_direction == direction:
#           box_counter+=1
#         direction = new_direction
#     print(box_counter)
#   if n>=2: turns.append((path[-1],'End'))
#   return turns