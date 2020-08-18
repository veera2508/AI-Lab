'''
Decantation Problem

States - Represented as (a,b,c) where a is water in bucket 1, b is water in bucket 2, c is water in bucket 3
Actions - Transfer water completely from one bucket to another bucket given it has sufficient capacity [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1)]
Initial State - (8,0,0)
Goal State - 4 in any one of the buckets

'''

from collections import deque

#Data structure to store each state and child
class state:
    def __init__(self, val, parent= None):
        self.val = val
        self.parent = parent

#Constants for the problem
capacity = (8, 5, 3)
actions = [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1)]
dis = set()

#Func to return list of all successor state for the given state
def next_states(s):
    nextstates = []
    for action in actions:
        ns = [p for p in s.val]
        if s.val[action[1]] < capacity[action[1]] and s.val[action[0]] >= 0:
            if s.val[action[0]] > (capacity[action[1]] - s.val[action[1]]):
                ns[action[0]] -= (capacity[action[1]] - s.val[action[1]])
                ns[action[1]] += (capacity[action[1]] - s.val[action[1]])
            else:
                ns[action[1]] += s.val[action[0]]
                ns[action[0]] = 0  
        if ns != s.val:
            nextstates.append(state(ns, s))
    return nextstates

#Func to check if goal state is reached
def goal(s):
    if 4 in s.val:
        return True
    else:
        return False

#Func to print the path
def printPath(s):
    lst = []
    while s!= None:
        lst.append(s.val)
        s = s.parent
    lst.reverse()
    for i in range(len(lst)-1):
        print(lst[i], end = '->')
    print(lst[i+1])
    print()


#Func for the bfs search
def bfs(s):
    q = deque()
    dis.add(s)
    q.append(s)
    while len(q) != 0:
        u = q.popleft()
        nextstates = next_states(u)
        for i in nextstates:
            if i not in dis:
                dis.add(i)
                if goal(i):
                    printPath(i)
                    print()
                    return
                q.append(i)
 

                    

print('Enter the initial state as space seperated integers (Total <= 8 and Individual values <= (8,5,3)):')
st = input().split(' ')
st = [int(i) for i in st]
bfs(state(st))






