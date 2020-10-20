import random
from copy import deepcopy

class twopenv:
    def __init__(self, b_size):
        self.size = b_size
        self.memory = {}
    
    def stateto2d(self, state):
        arr = [[0 for j in range(self.size)] for i in range(self.size)]
        i = 0
        j = 0
        for p in state:
            arr[i][j] = p
            j += 1
            if j > self.size - 1:
                j = 0
                i += 1
        return arr
    
    def checkrow(self, state):
        n = self.size
        for i in range(n):
            srow = True
            p = state[i][0]
            for j in range(1, n):
                if (state[i][j] != p):
                    srow = False
            if srow == True:
                return True, p
        return False, None

    def checkcol(self, state):
        n = self.size
        for i in range(n):
            scol = True
            p = state[0][i]
            for j in range(1, n):
                if (state[j][i] != p):
                    scol = False
            if scol == True:
                return True, p
        return False, None
    
    def checkdiag(self, state):
        n = self.size
        sdiag = True
        ssdiag = True
        p = state[0][0]
        q = state[0][n-1]
        for i in range(1, n):
            if (state[i][i] != p):
                sdiag = False
            if (state[i][n-1-i] != q):
                ssdiag = False
        if sdiag == True:
            return True, p
        if ssdiag == True:
            return True, q
        return False, None

    def goal(self, state):
        arr = self.stateto2d(state)
        isrow, val = self.checkrow(arr)
        if (isrow and val != 0):
            return True, val
        iscol, val = self.checkcol(arr)
        if (iscol and val != 0):
            return True, val
        isdiag, val = self.checkdiag(arr)
        if (isdiag and val != 0):
            return True, val
        isdraw = True
        for i in state:
            if i == 0:
                isdraw = False
                break
        if isdraw:
            return True, 0
        return False, 0
    
    def next_moves(self, state, previous):
        next_states = []
        for i, j in enumerate(state):
            if j == 0:
                newstate = deepcopy(state)
                newstate[i] = -1 * previous
                next_states.append(newstate)
        return next_states

        
        