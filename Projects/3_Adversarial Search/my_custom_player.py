from sample_players import BasePlayer

import pickle
import random
import itertools


class BaselinePlayer(BasePlayer):
    def get_action(self, state):
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            d = 1
            while(True):
                # print(d)
                self.queue.put(self.ab_search(state, depth=d))
                d += 1

    def ab_search(self, state, depth):
        def get_min(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, get_max(
                    state.result(action), alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                else:
                    beta = min(beta, value)
            return value

        def get_max(state, alpha, beta, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, get_min(
                    state.result(action), alpha, beta, depth - 1))
                if value >= beta:
                    return value
                else:
                    alpha = max(alpha, value)
            return value

        alpha = float("-inf")
        beta = float("+inf")
        best_score = float("-inf")
        best_move = None

        for a in state.actions():
            v = get_min(state.result(a), alpha, beta, depth - 1)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_move = a

                # return a random move if no best_move is found
        if not best_move:
            best_move = random.choice(state.actions())

        return best_move

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)


class CustomPlayer(BaselinePlayer):
    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties)


class OffensivePlayer(BaselinePlayer):
    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - 2 * len(opp_liberties)
