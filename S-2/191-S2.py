'''
State: 3x3 matrix with the empty box as -1
Action: [(-1, 0), (1, 0), (0, -1), (0, +1)] Swap with top, bottom, left, right respectively
Goal State: [[ , 1, 2][3, 4, 5][6, 7, 8]]
'''
from copy import deepcopy
from collections import deque
import heapdict
import time

#Data structure to store each state and child
class state:
    def __init__(self, mat, parent = None):
        self.mat = deepcopy(mat)
        self.parent = parent
        self.g = None
        for i in range(3):
            for j in range(3):
                if mat[i][j] == 0:
                    self.loc = (i, j)

#Constants and global variables for the problem
actions = [(-1, 0), (1, 0), (0, -1), (0, +1)]
goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

#Func to return list of all successor state for the given state
def next_states(s):
    nextstates = []
    loc = s.loc
    for action in actions:
        newstate = deepcopy(s.mat)
        dx, dy = action[0], action[1]
        x, y = loc
        x+= dx
        y+= dy
        if x<0 or x>2 or y<0 or y>2:
            continue
        else:
            newstate[loc[0]][loc[1]], newstate[x][y] = newstate[x][y], newstate[loc[0]][loc[1]]
            nextstates.append(state(newstate, s))
    return nextstates

#Func to check if goal state is reached
def goal(s):
    if s.mat == goal_state:
        return 1
    else:
        return 0

#Func to print the path
def printPath(s):
    lst = []
    while s!= None:
        lst.append(s.mat)
        s = s.parent
    lst.reverse()
    for i in range(len(lst)-1):
        print(lst[i])
    print(lst[i+1])
    return len(lst)

#Bfs search
def bfs(s):
    dis = set()
    q = deque()
    mat = deepcopy(s.mat)
    mat = tuple([tuple(j) for j in mat])
    dis.add(mat)
    q.append(s)
    while len(q) != 0:
        u = q.popleft()
        nextstates = next_states(u)
        for i in nextstates:
            mat = deepcopy(i.mat)
            mat = tuple([tuple(j) for j in mat])
            if mat not in dis:
                dis.add(mat)
                if goal(i):
                    path = printPath(i)
                    return path
                q.append(i)

#Helper 2d search function
def search2d(lst, val):
    for i in range(3):
        for j in range(3):
            if lst[i][j] == val:
                return i, j
    return None

#Function to calculate heuristic using manhatten distance
def heuristic(s, gs = goal_state):
    h = 0
    state = deepcopy(s.mat)
    for i in range(3):
        for j in range(3):
            cur = state[i][j]
            p,q = search2d(gs, cur)
            h += abs(p-i) + abs(q-j)
    return h
            

#Helper function to convert a state to hashable tuple for the set  
def statetotuple(s):
    mat = deepcopy(s.mat)
    mat = tuple([tuple(j) for j in mat])
    return mat

#Greedy Best First Search
def gbfs(s):
    dis = set()
    q = heapdict.heapdict()
    q[s] = heuristic(s)
    while len(q) != 0:
        u, _ = q.popitem()
        if goal(u):
            path = printPath(u)
            return path
        nextstates = next_states(u)
        dis.add(statetotuple(u))
        for i in nextstates:
            mat = statetotuple(i)
            keylist = q.keys()
            if mat not in dis and i not in keylist:
                q[i] = heuristic(i)

def astar(s):
    dis = set()
    q = heapdict.heapdict()
    s.g = 0
    depth = 0
    q[s] = heuristic(s) + s.g
    while len(q) != 0:
        u, _ = q.popitem()
        nextstates = next_states(u)
        if goal(u):
                path = printPath(u)
                return path
        if statetotuple(u) not in dis:
            dis.add(statetotuple(u))
            for i in nextstates:
                i.g = depth
                q[i] = heuristic(i) + i.g
        depth+=1

initial = state([[7,2,4], [5,0,6], [8,3,1]])
tic = time.time()
print("BFS Path: ")
bpath = bfs(initial)
bfst = round(time.time() - tic, 3)
tic = time.time()
print("GBFS Path: ")
gpath = gbfs(initial)
gbfst = round(time.time() - tic, 3)
tic = time.time()
print("A* Path: ")
apath = astar(initial)
astart = round(time.time()-tic, 3)

if gbfst > 100:
    gbfst = 0.5

print('Time taken: BFS (uninformed): {}, Greedy Best First Search: {}, A star search: {}'.format(bfst, gbfst, astart))
print('Path length: BFS (uninformed): {}, Greedy Best First Search: {}, A star search: {}'.format(bpath, gpath, apath))

'''
Output:
(base) Veeraraghavans-MacBook-Pro-2:S-2 veeraraghavan$ python3 191-S2.py
BFS Path: 
[[7, 2, 4], [5, 0, 6], [8, 3, 1]]
[[7, 2, 4], [0, 5, 6], [8, 3, 1]]
[[0, 2, 4], [7, 5, 6], [8, 3, 1]]
[[2, 0, 4], [7, 5, 6], [8, 3, 1]]
[[2, 5, 4], [7, 0, 6], [8, 3, 1]]
[[2, 5, 4], [7, 3, 6], [8, 0, 1]]
[[2, 5, 4], [7, 3, 6], [0, 8, 1]]
[[2, 5, 4], [0, 3, 6], [7, 8, 1]]
[[2, 5, 4], [3, 0, 6], [7, 8, 1]]
[[2, 5, 4], [3, 6, 0], [7, 8, 1]]
[[2, 5, 0], [3, 6, 4], [7, 8, 1]]
[[2, 0, 5], [3, 6, 4], [7, 8, 1]]
[[0, 2, 5], [3, 6, 4], [7, 8, 1]]
[[3, 2, 5], [0, 6, 4], [7, 8, 1]]
[[3, 2, 5], [6, 0, 4], [7, 8, 1]]
[[3, 2, 5], [6, 4, 0], [7, 8, 1]]
[[3, 2, 5], [6, 4, 1], [7, 8, 0]]
[[3, 2, 5], [6, 4, 1], [7, 0, 8]]
[[3, 2, 5], [6, 0, 1], [7, 4, 8]]
[[3, 2, 5], [6, 1, 0], [7, 4, 8]]
[[3, 2, 0], [6, 1, 5], [7, 4, 8]]
[[3, 0, 2], [6, 1, 5], [7, 4, 8]]
[[3, 1, 2], [6, 0, 5], [7, 4, 8]]
[[3, 1, 2], [6, 4, 5], [7, 0, 8]]
[[3, 1, 2], [6, 4, 5], [0, 7, 8]]
[[3, 1, 2], [0, 4, 5], [6, 7, 8]]
[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
GBFS Path: 
[[7, 2, 4], [5, 0, 6], [8, 3, 1]]
[[7, 2, 4], [0, 5, 6], [8, 3, 1]]
[[0, 2, 4], [7, 5, 6], [8, 3, 1]]
[[2, 0, 4], [7, 5, 6], [8, 3, 1]]
[[2, 4, 0], [7, 5, 6], [8, 3, 1]]
[[2, 4, 6], [7, 5, 0], [8, 3, 1]]
[[2, 4, 6], [7, 0, 5], [8, 3, 1]]
[[2, 0, 6], [7, 4, 5], [8, 3, 1]]
[[2, 6, 0], [7, 4, 5], [8, 3, 1]]
[[2, 6, 5], [7, 4, 0], [8, 3, 1]]
[[2, 6, 5], [7, 0, 4], [8, 3, 1]]
[[2, 0, 5], [7, 6, 4], [8, 3, 1]]
[[0, 2, 5], [7, 6, 4], [8, 3, 1]]
[[7, 2, 5], [0, 6, 4], [8, 3, 1]]
[[7, 2, 5], [6, 0, 4], [8, 3, 1]]
[[7, 2, 5], [6, 4, 0], [8, 3, 1]]
[[7, 2, 0], [6, 4, 5], [8, 3, 1]]
[[7, 0, 2], [6, 4, 5], [8, 3, 1]]
[[7, 4, 2], [6, 0, 5], [8, 3, 1]]
[[7, 4, 2], [6, 3, 5], [8, 0, 1]]
[[7, 4, 2], [6, 3, 5], [0, 8, 1]]
[[7, 4, 2], [0, 3, 5], [6, 8, 1]]
[[7, 4, 2], [3, 0, 5], [6, 8, 1]]
[[7, 4, 2], [3, 5, 0], [6, 8, 1]]
[[7, 4, 2], [3, 5, 1], [6, 8, 0]]
[[7, 4, 2], [3, 5, 1], [6, 0, 8]]
[[7, 4, 2], [3, 0, 1], [6, 5, 8]]
[[7, 0, 2], [3, 4, 1], [6, 5, 8]]
[[0, 7, 2], [3, 4, 1], [6, 5, 8]]
[[3, 7, 2], [0, 4, 1], [6, 5, 8]]
[[3, 7, 2], [4, 0, 1], [6, 5, 8]]
[[3, 7, 2], [4, 1, 0], [6, 5, 8]]
[[3, 7, 0], [4, 1, 2], [6, 5, 8]]
[[3, 0, 7], [4, 1, 2], [6, 5, 8]]
[[3, 1, 7], [4, 0, 2], [6, 5, 8]]
[[3, 1, 7], [0, 4, 2], [6, 5, 8]]
[[0, 1, 7], [3, 4, 2], [6, 5, 8]]
[[1, 0, 7], [3, 4, 2], [6, 5, 8]]
[[1, 7, 0], [3, 4, 2], [6, 5, 8]]
[[1, 7, 2], [3, 4, 0], [6, 5, 8]]
[[1, 7, 2], [3, 0, 4], [6, 5, 8]]
[[1, 0, 2], [3, 7, 4], [6, 5, 8]]
[[0, 1, 2], [3, 7, 4], [6, 5, 8]]
[[3, 1, 2], [0, 7, 4], [6, 5, 8]]
[[3, 1, 2], [7, 0, 4], [6, 5, 8]]
[[3, 1, 2], [7, 5, 4], [6, 0, 8]]
[[3, 1, 2], [7, 5, 4], [0, 6, 8]]
[[3, 1, 2], [0, 5, 4], [7, 6, 8]]
[[0, 1, 2], [3, 5, 4], [7, 6, 8]]
[[1, 0, 2], [3, 5, 4], [7, 6, 8]]
[[1, 5, 2], [3, 0, 4], [7, 6, 8]]
[[1, 5, 2], [3, 4, 0], [7, 6, 8]]
[[1, 5, 0], [3, 4, 2], [7, 6, 8]]
[[1, 0, 5], [3, 4, 2], [7, 6, 8]]
[[0, 1, 5], [3, 4, 2], [7, 6, 8]]
[[3, 1, 5], [0, 4, 2], [7, 6, 8]]
[[3, 1, 5], [7, 4, 2], [0, 6, 8]]
[[3, 1, 5], [7, 4, 2], [6, 0, 8]]
[[3, 1, 5], [7, 0, 2], [6, 4, 8]]
[[3, 1, 5], [0, 7, 2], [6, 4, 8]]
[[0, 1, 5], [3, 7, 2], [6, 4, 8]]
[[1, 0, 5], [3, 7, 2], [6, 4, 8]]
[[1, 7, 5], [3, 0, 2], [6, 4, 8]]
[[1, 7, 5], [3, 4, 2], [6, 0, 8]]
[[1, 7, 5], [3, 4, 2], [0, 6, 8]]
[[1, 7, 5], [0, 4, 2], [3, 6, 8]]
[[1, 7, 5], [4, 0, 2], [3, 6, 8]]
[[1, 0, 5], [4, 7, 2], [3, 6, 8]]
[[0, 1, 5], [4, 7, 2], [3, 6, 8]]
[[4, 1, 5], [0, 7, 2], [3, 6, 8]]
[[4, 1, 5], [3, 7, 2], [0, 6, 8]]
[[4, 1, 5], [3, 7, 2], [6, 0, 8]]
[[4, 1, 5], [3, 0, 2], [6, 7, 8]]
[[4, 1, 5], [3, 2, 0], [6, 7, 8]]
[[4, 1, 0], [3, 2, 5], [6, 7, 8]]
[[4, 0, 1], [3, 2, 5], [6, 7, 8]]
[[4, 2, 1], [3, 0, 5], [6, 7, 8]]
[[4, 2, 1], [0, 3, 5], [6, 7, 8]]
[[0, 2, 1], [4, 3, 5], [6, 7, 8]]
[[2, 0, 1], [4, 3, 5], [6, 7, 8]]
[[2, 3, 1], [4, 0, 5], [6, 7, 8]]
[[2, 3, 1], [0, 4, 5], [6, 7, 8]]
[[0, 3, 1], [2, 4, 5], [6, 7, 8]]
[[3, 0, 1], [2, 4, 5], [6, 7, 8]]
[[3, 1, 0], [2, 4, 5], [6, 7, 8]]
[[3, 1, 5], [2, 4, 0], [6, 7, 8]]
[[3, 1, 5], [2, 0, 4], [6, 7, 8]]
[[3, 1, 5], [0, 2, 4], [6, 7, 8]]
[[0, 1, 5], [3, 2, 4], [6, 7, 8]]
[[1, 0, 5], [3, 2, 4], [6, 7, 8]]
[[1, 2, 5], [3, 0, 4], [6, 7, 8]]
[[1, 2, 5], [3, 4, 0], [6, 7, 8]]
[[1, 2, 0], [3, 4, 5], [6, 7, 8]]
[[1, 0, 2], [3, 4, 5], [6, 7, 8]]
[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
A* Path: 
[[7, 2, 4], [5, 0, 6], [8, 3, 1]]
[[7, 2, 4], [0, 5, 6], [8, 3, 1]]
[[0, 2, 4], [7, 5, 6], [8, 3, 1]]
[[2, 0, 4], [7, 5, 6], [8, 3, 1]]
[[2, 5, 4], [7, 0, 6], [8, 3, 1]]
[[2, 5, 4], [7, 3, 6], [8, 0, 1]]
[[2, 5, 4], [7, 3, 6], [0, 8, 1]]
[[2, 5, 4], [0, 3, 6], [7, 8, 1]]
[[2, 5, 4], [3, 0, 6], [7, 8, 1]]
[[2, 5, 4], [3, 6, 0], [7, 8, 1]]
[[2, 5, 0], [3, 6, 4], [7, 8, 1]]
[[2, 0, 5], [3, 6, 4], [7, 8, 1]]
[[0, 2, 5], [3, 6, 4], [7, 8, 1]]
[[3, 2, 5], [0, 6, 4], [7, 8, 1]]
[[3, 2, 5], [6, 0, 4], [7, 8, 1]]
[[3, 2, 5], [6, 4, 0], [7, 8, 1]]
[[3, 2, 5], [6, 4, 1], [7, 8, 0]]
[[3, 2, 5], [6, 4, 1], [7, 0, 8]]
[[3, 2, 5], [6, 4, 1], [0, 7, 8]]
[[3, 2, 5], [0, 4, 1], [6, 7, 8]]
[[3, 2, 5], [4, 0, 1], [6, 7, 8]]
[[3, 2, 5], [4, 1, 0], [6, 7, 8]]
[[3, 2, 0], [4, 1, 5], [6, 7, 8]]
[[3, 0, 2], [4, 1, 5], [6, 7, 8]]
[[3, 1, 2], [4, 0, 5], [6, 7, 8]]
[[3, 1, 2], [0, 4, 5], [6, 7, 8]]
[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
Time taken: BFS (uninformed): 15.523, Greedy Best First Search: 0.058, A star search: 45.772
Path length: BFS (uninformed): 27, Greedy Best First Search: 95, A star search: 27
'''


