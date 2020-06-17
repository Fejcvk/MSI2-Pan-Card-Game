import math
import random
from Card import Card
from Move import Move
from UctPlayer import UctPlayer


def ind_max(x):
    m = max(x)
    return x.index(m)


class UCB1Player(UctPlayer):

    def __init__(self, pulls, values, id: int):
        super().__init__(id)
        self.pulls = pulls
        self.values = values

    def initialize(self, number_of_arms: int):
        self.pulls = [0 for i in range(number_of_arms)]
        self.values = [0.0 for i in range(number_of_arms)]

    def select_arm(self, available_states):

        for arm in available_states:
            if self.pulls[arm] == 0:
                return arm
        ucb1_values = [0.0 for arm in range(max(available_states) + 1)]
        total_pulls = sum(self.pulls)

        for arm in available_states:
            ucb1_values[arm] = self.values[arm] + math.sqrt((2 * math.log(total_pulls)) / float(self.pulls[arm]))
        res = ind_max(ucb1_values)
        return res

    def update(self, chosen_arm, reward):
        if chosen_arm >= len(self.pulls):
            self.pulls.append(1)
            self.values.append(0.0)

        else:
            self.pulls[chosen_arm] = self.pulls[chosen_arm] + 1

        n = self.pulls[chosen_arm]

        value = self.values[chosen_arm]
        new_val = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_val

    def move(self, pile: [Card], is_starting_move=False):
        if is_starting_move:
            return super().move(pile, is_starting_move)
        list_of_moves = super().list_possible_moves(pile=pile)
        if not self.make_random_move:
            list_of_states_after_moves = self.make_list_of_states_after_moves(pile, list_of_moves)
            for idx, state in enumerate(list_of_states_after_moves):
                if state not in self.visited_states:
                    self.make_random_move = True
                    self.visited_states.append(state)
                    self.number_of_visits.append(1)
                    self.visited_states_in_current_game.append(state)
                    self.number_of_successes.append(0)
                    self.number_of_moves += 1
                    return super().execute_move(move=list_of_moves[idx], pile=pile)

            available_states = []
            for state in self.visited_states:
                for after_state in list_of_states_after_moves:
                    if state == after_state:
                        available_states.append(self.visited_states.index(state))

            idx = self.select_arm(available_states)
            idx = list_of_states_after_moves.index(self.visited_states[idx])
            self.number_of_visits[idx] += 1
            self.number_of_moves += 1
            self.visited_states_in_current_game.append(self.visited_states[idx])
            return super().execute_move(move=list_of_moves[idx], pile=pile)
        else:
            return super().execute_move(move=random.choice(list_of_moves), pile=pile)

    def update_graphs_after_result(self, win: bool):
        for state in self.visited_states_in_current_game:
            idx = self.visited_states.index(state)
            if win:
                self.update(idx, 1.0)
            else:
                self.update(idx, 0.0)
        self.visited_states_in_current_game = []
        self.cards = []
        self.make_random_move = False
