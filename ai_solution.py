import game as game
from queue import PriorityQueue
from copy import deepcopy

class GameSolution:
    def __init__(self, game):
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = []  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = game.NEmptyTubes + game.NColor  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = set()  # A set of visited tubes.

    def solve(self, current_state):
        
        if(self.ws_game.check_victory(current_state)):
            self.solution_found = True
            return
        else:
            for this in range(len(current_state)):
                for that in range(len(current_state)):
                    if this != that:  
                        length = 1
                        chain = True 
                        color_on_top = 100
                        color_to_move = 100 
                        if len(current_state[this]) > 0:
                            color_to_move = current_state[this][-1]
                            for col in range(1, len(current_state[this])):
                                if chain:
                                    if current_state[this][-1 - col] == color_to_move:
                                        length += 1
                                    else:
                                        chain = False
                        if len(current_state[that]) < self.ws_game.NColorInTube:
                            if len(current_state[that]) == 0:
                                color_on_top = color_to_move
                            else:
                                color_on_top = current_state[that][-1]
                        if color_to_move == color_on_top and len(current_state[this])>0:
                                if this != that:
                                    new_st = deepcopy(current_state)
                                    if len(new_st[that]) < self.ws_game.NColorInTube and len(new_st[this]) > 0:
                                        if length <= self.ws_game.NColorInTube - len(new_st[that]):
                                            if length > 1 :
                                                for i in range(length):
                                                    new_st[that].append(color_to_move)
                                            else:
                                                new_st[that].append(color_to_move)
                                            if length>1:
                                                for i in range(length):
                                                    new_st[this].pop(-1)
                                            else:
                                                new_st[this].pop(-1)
                                            if tuple(map(tuple, new_st)) not in self.visited_tubes:
                                                self.visited_tubes.add(tuple(map(tuple, new_st)))
                                                self.moves.append((this,that))
                                                current_state = new_st
                                                self.solve(current_state)
            
                                                if self.solution_found:
                                                    return True
                                                else:
                                                    self.moves.remove((this,that))
                                                    return False
                        
            
    def optimal_solve(self, current_state):
        sp = PriorityQueue()
        h = {}
        g = {tuple(map(tuple, current_state)): 0}
        self.visited_tubes = set()

        sp.put((self.heuristic(current_state), current_state, [])) 

        while(not sp.empty()):
            _, current_state, current_moves = sp.get()
            if self.ws_game.check_victory(current_state):
                self.moves = current_moves
                self.solution_found = True
                return
            

            self.visited_tubes.add(tuple(map(tuple, current_state)))


            for this in range(len(current_state)):
                for that in range(len(current_state)):
                    if this != that:
                        length = 1
                        chain = True
                        color_to_move = 100
                        if len(current_state[this]) > 0:
                            color_to_move = current_state[this][-1]
                            for col in range(1, len(current_state[this])):
                                if chain and current_state[this][-1 - col] == color_to_move:
                                    length += 1
                                else:
                                    chain = False
                        if len(current_state[that]) < self.ws_game.NColorInTube and len(current_state[this]) > 0:
                            if (len(current_state[that]) == 0 or current_state[that][-1] == color_to_move):
                                new_st = deepcopy(current_state)
                                for i in range(length):
                                    if len(new_st[that]) < self.ws_game.NColorInTube:
                                        new_st[that].append(color_to_move)
                                        new_st[this].pop(-1)
                                if tuple(map(tuple, new_st)) not in self.visited_tubes:
                                        new_g = g[tuple(map(tuple, current_state))] + 1
                                        new_h = self.heuristic(new_st)
                                        priority = new_g + new_h
                                        sp.put((priority, new_st, current_moves + [(this, that)]))
                                        g[tuple(map(tuple, new_st))] = new_g

    def heuristic(self, states):
        ms = 0
        for tube in states:
            if len(tube) > 0:
                unique_colors = set(tube)
                if len(unique_colors) > 1:
                    ms += len(tube)
        return ms



