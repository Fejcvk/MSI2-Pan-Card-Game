import copy
import math
import random
from Player import Player
from Card import Card
from Move import Move, ActionType
from State import State


class UctPlayer(Player):
    def __init__(self, id: int):
        super().__init__(id)
        self.state = State
        self.visited_states = []
        self.number_of_visits = []
        self.number_of_successes = []
        self.visited_states_in_current_game = []
        self.number_of_moves = 0
        self.make_random_move = False
        self.number_of_moves_in_current_game = 0

    def move(self, pile: [Card], is_starting_move=False):
        if is_starting_move:
            return super().move(pile, is_starting_move)
        list_of_moves = super().list_possible_moves(pile=pile)
        if not self.make_random_move and self.number_of_moves_in_current_game < 10:
            list_of_states_after_moves = self.make_list_of_states_after_moves(pile, list_of_moves)
            uct_moves_values = []
            for idx, state in enumerate(list_of_states_after_moves):
                if state not in self.visited_states:
                    self.make_random_move = True
                    self.visited_states.append(state)
                    self.number_of_visits.append(1)
                    self.visited_states_in_current_game.append(state)
                    self.number_of_successes.append(0)
                    self.number_of_moves += 1
                    return super().execute_move(move=list_of_moves[idx], pile=pile)
                else:
                    idx = self.visited_states.index(state)
                    uct_moves_values.append(self.calculate_uct_move_value(idx))
            max_uct_value = max(uct_moves_values)
            max_uct_value_idx = uct_moves_values.index(max_uct_value)
            self.number_of_visits[max_uct_value_idx] += 1
            self.number_of_moves += 1
            self.visited_states_in_current_game.append(list_of_states_after_moves[max_uct_value_idx])
            return super().execute_move(move=list_of_moves[max_uct_value_idx], pile=pile)
        else:
            super().execute_move(move=random.choice(list_of_moves), pile=pile)

    def make_list_of_states_after_moves(self, pile: [Card], list_of_moves: [Move]):
        list_of_states = []
        for move in list_of_moves:
            state = copy.copy(self.state)
            tmp_pile = copy.copy(pile)
            if move.action_type == ActionType.DRAW:
                for i in range(min(len(pile) - 1, 3)):
                    card_to_draw = tmp_pile.pop()
                    state = self.change_state(state=state, card=card_to_draw.value, draw=True)
            else:
                for i in range(move.number_of_actionable_cards):
                    state = self.change_state(state=state, card=move.card_value, draw=False)
            list_of_states.append(state)
        return list_of_states

    def calculate_uct_move_value(self, idx):
        q_s = self.number_of_successes[idx] / self.number_of_visits[idx]
        c = 1.414
        sqrt = math.sqrt(math.log(self.number_of_visits[idx]) / self.number_of_moves)
        return q_s + c * sqrt

    def change_state(self, state: State, card: int, draw: bool):
        if draw:
            add_to_pile = -1
            add_to_hand = 1
        else:
            add_to_pile = 1
            add_to_hand = -1
        if card == 9:
            state.number_o_nines = state.number_of_nines + add_to_hand
            state.number_of_nines_on_pile = state.number_of_nines_on_pile + add_to_pile
        if card == 10:
            state.number_of_tens = state.number_of_tens + add_to_hand
            state.number_of_tens_on_pile = state.number_of_tens_on_pile + add_to_pile
        if card == 11:
            state.number_of_jacks = state.number_of_jacks + add_to_hand
            state.number_of_jacks_on_pile = state.number_of_jacks_on_pile + add_to_pile
        if card == 12:
            state.number_of_queens = state.number_of_queens + add_to_hand
            state.number_of_queens_on_pile = state.number_of_queens_on_pile + add_to_pile
        if card == 13:
            state.number_of_kings = state.number_of_kings + add_to_hand
            state.number_of_kings_on_pile = state.number_of_kings_on_pile + add_to_pile
        if card == 14:
            state.number_of_aces = state.number_of_kings + add_to_hand
            state.number_of_aces_on_pile = state.number_of_kings_on_pile + add_to_pile
        return state

    def get_state(self):
        number_of_nines = 0
        number_of_tens = 0
        number_of_jacks = 0
        number_of_queens = 0
        number_of_kings = 0
        number_of_aces = 0

        for card in self.cards:
            if card.value == 9:
                number_of_nines += 1
            if card.value == 10:
                number_of_tens += 1
            if card.value == 11:
                number_of_jacks += 1
            if card.value == 12:
                number_of_queens += 1
            if card.value == 13:
                number_of_kings += 1
            if card.value == 14:
                number_of_aces += 1
        self.state = State(number_of_nines, number_of_tens, number_of_jacks, number_of_queens, number_of_kings,
                           number_of_aces, number_of_nines_on_pile=1, number_of_tens_on_pile=0,
                           number_of_jacks_on_pile=0, number_of_queens_on_pile=0, number_of_kings_on_pile=0,
                           number_of_aces_on_pile=0)

    def update_graphs_after_result(self, win: bool):
        for state in self.visited_states_in_current_game:
            idx = self.visited_states.index(state)
            if win:
                self.number_of_successes[idx] += 1
        self.visited_states_in_current_game = []
        self.cards = []
        self.make_random_move = False
