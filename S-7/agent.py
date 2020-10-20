from env import twopenv

class game:
    def __init__(self, env):
        self.memory = {}
        self.env = env
    
    def findmin(self, state):
        isgoal, val = self.env.goal(state)
        if (isgoal):
            self.memory[tuple(state)] = val
            return val
        if tuple(state) in self.memory:
            return self.memory[tuple(state)]
        next_moves = self.env.next_moves(state, -1)
        val = -100
        for move in next_moves:
            self.memory[tuple(move)] = self.findmax(move)
            val = min(val, self.memory[tuple(move)])
        return val
    
    def findmax(self, state):
        isgoal, val = self.env.goal(state)
        if (isgoal):
            self.memory[tuple(state)] = val
            return val
        if tuple(state) in self.memory:
            return self.memory[tuple(state)]
        next_moves = self.env.next_moves(state, 1)
        val = 100
        for move in next_moves:
            self.memory[tuple(move)] = self.findmin(move)
            val = max(val, self.memory[tuple(move)])
        return val
    
    def decision(self, state):
        maxi = 1000
        next_state = []
        next_moves = self.env.next_moves(state, -1)
        for move in next_moves:
            val = self.findmax(move)
            if (maxi > val):
                maxi = val
                next_state = move
        return next_state
    
    def play(self):
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        while True:
            print(state)
            isgoal, winner = self.env.goal(state)
            if (isgoal):
                print(winner)
                break
            print("Enter the move (1-9): ")
            m = int(input())
            state[m] = -1
            state = self.decision(state)

env = twopenv(3)
state = [1, 0, 1, 1, 0 , -1, 1, -1, -1]
gm = game(env)
gm.play()
