'''
State: 1D array where index represents the row and value represents the column of the queen
Action: Move each queen one column left or right
Cost Function (Minimize): No of attacking queens
'''

import random
from copy import deepcopy
import time

def configtoarray(config):
    arr = [[0 for j in range(len(config))] for i in range(len(config))]
    for i, j in enumerate(config):
        arr[i][j] = 1
    return arr

def checkcols(arr, i, j):
    cost = 0
    for p in range(len(arr[0])):
        if p == i:
            continue
        cost += arr[p][j]
    return cost

def checkud(arr, i, j):
    cost = 0
    l = len(arr[0])
    m , n = i-1, j-1
    while m >= 0 and n >= 0:
        cost += arr[m][n]
        m -= 1
        n -= 1
    m, n = i+1, j+1
    while m < l and n < l:
        cost += arr[m][n]
        m += 1
        n += 1
    return cost

def checkld(arr, i, j):
    cost = 0
    l = len(arr[0])
    m , n = i-1, j+1
    while m >= 0 and n < l:
        cost += arr[m][n]
        m -= 1
        n += 1
    m, n = i+1, j-1
    while m < l and n >= 0:
        cost += arr[m][n]
        m += 1
        n -= 1
    return cost


def cost(config):
    arr = configtoarray(config)
    cost = 0
    for i, j in enumerate(config):
        col = checkcols(arr, i, j)
        ud = checkud(arr, i, j)
        ld = checkld(arr, i, j)
        cost += col + ud + ld
    return cost//2
        

def randconfig():
    config = [random.randint(0,8) for i in range(9)]
    return config

def getlow(config):
    actionvals = []
    curcst = cost(config)
    for i in range(len(config)):
        temp = deepcopy(config)
        for j in range(len(config)):
            if j == config[i]:
                continue
            temp[i] = j
            if temp != config:
                cst = cost(temp)
                if cst <= curcst:
                    actionvals.append((temp, cst))
    
    if not actionvals:
        return config
    minconfig, mincost = actionvals[0]
    for i in range(1, len(actionvals)):
        con, cst = actionvals[i]
        if cst < mincost:
            mincost = cst
            minconfig = con
    return minconfig, mincost

def hillclimb(config = None):
    if not config:
        config = randconfig()
    cst = cost(config)
    i = 0
    pcst = 0
    j = 0
    while True:
        config, cst = getlow(config)
        if cst == 0 or not cst:
            return config
        if pcst == cst:
            i += 1
        else:
            pcst = cst
        if i == 1000:
            break
        
        j += 1
    return config, cst

def search(iterations):
    for i in range(iterations):
        config, cst = hillclimb()
        print(i, config, cst)
        if cst == 0:
            print("Solution Found")

search(10)



            



