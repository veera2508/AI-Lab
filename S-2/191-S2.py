'''
State: 3x3 matrix with the empty box as -1
Action: [(-1, 0), (1, 0), (0, -1), (0, +1)] Swap with top, bottom, left, right respectively
Goal State: [[ , 1, 2][3, 4, 5][6, 7, 8]]
'''
from copy import deepcopy
from collections import deque

#Data structure to store each state and child
class state:
    def __init__(self, mat, parent = None):
        self.mat = deepcopy(mat)
        self.parent = parent
        for i in range(3):
            for j in range(3):
                if mat[i][j] == -1:
                    self.loc = (i, j)

#Constants and global variables for the problem
actions = [(-1, 0), (1, 0), (0, -1), (0, +1)]
dis = set()

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
    mat = deepcopy(s.mat)
    count = 0
    
    for i in range(3):
        for j in range(3):
            if i==0 and j==0:
                if mat[i][j] == -1:
                    count = 1
            elif mat[i][j] == count:
                count+= 1
            else:
                return 0
    return 1

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
    print()

#Func for the bfs search
def bfs(s):
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
                    printPath(i)
                    print()
                    return
                q.append(i)



bfs(state([[7,2,4], [5,-1,6], [8,3,1]]))

'''
Output for [[7,2,4], 
            [5,-1,6], 
            [8,3,1]]
(takes time to get the output depending on system speed)

[7, 2, 4], [5, -1, 6], [8, 3, 1]]
[[7, 2, 4], [-1, 5, 6], [8, 3, 1]]
[[-1, 2, 4], [7, 5, 6], [8, 3, 1]]
[[2, -1, 4], [7, 5, 6], [8, 3, 1]]
[[2, 5, 4], [7, -1, 6], [8, 3, 1]]
[[2, 5, 4], [7, 3, 6], [8, -1, 1]]
[[2, 5, 4], [7, 3, 6], [-1, 8, 1]]
[[2, 5, 4], [-1, 3, 6], [7, 8, 1]]
[[2, 5, 4], [3, -1, 6], [7, 8, 1]]
[[2, 5, 4], [3, 6, -1], [7, 8, 1]]
[[2, 5, -1], [3, 6, 4], [7, 8, 1]]
[[2, -1, 5], [3, 6, 4], [7, 8, 1]]
[[-1, 2, 5], [3, 6, 4], [7, 8, 1]]
[[3, 2, 5], [-1, 6, 4], [7, 8, 1]]
[[3, 2, 5], [6, -1, 4], [7, 8, 1]]
[[3, 2, 5], [6, 4, -1], [7, 8, 1]]
[[3, 2, 5], [6, 4, 1], [7, 8, -1]]
[[3, 2, 5], [6, 4, 1], [7, -1, 8]]
[[3, 2, 5], [6, -1, 1], [7, 4, 8]]
[[3, 2, 5], [6, 1, -1], [7, 4, 8]]
[[3, 2, -1], [6, 1, 5], [7, 4, 8]]
[[3, -1, 2], [6, 1, 5], [7, 4, 8]]
[[3, 1, 2], [6, -1, 5], [7, 4, 8]]
[[3, 1, 2], [6, 4, 5], [7, -1, 8]]
[[3, 1, 2], [6, 4, 5], [-1, 7, 8]]
[[3, 1, 2], [-1, 4, 5], [6, 7, 8]]
[[-1, 1, 2], [3, 4, 5], [6, 7, 8]]
'''

