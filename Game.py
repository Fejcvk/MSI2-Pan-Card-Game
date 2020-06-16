from datetime import datetime

from Player import Player
from Card import Card, card_values
from UctPlayer import UctPlayer
import random
import pickle
import pandas as pd

PRINT = False

class Game:

    def __init__(self):
        self.p1 = UctPlayer(id=1)
        self.p2 = UctPlayer(id=2)
        self.amount_of_cards = 24
        self.number_of_players = 2
        self.number_of_card_colors = 4
        self.deck = []
        self.create_new_game()
        self.card_pile = []

    def create_deck_of_cards(self) -> [Card]:

        deck = []

        for i in range(0, self.number_of_card_colors):
            for value in card_values.keys():
                card = Card(value=value, color=i)
                deck.append(card)
        return deck

    def distribute_cards_among_players(self):
        random.shuffle(self.deck)
        is_even = False

        for card in self.deck:
            if is_even:
                self.p1.add_card(card)
            if not is_even:
                self.p2.add_card(card)
            is_even = not is_even

    def create_new_game(self):
        self.deck = self.create_deck_of_cards()
        self.distribute_cards_among_players()
        if PRINT:
            print("Player 1 cards")
        self.p1.list_cards(show_colors=True)
        if PRINT:
            print('\n')
            print("Player 2 cards")
        self.p2.list_cards(show_colors=True)
        if PRINT:
            print('\n')

    def select_starting_player(self) -> Player:

        nine_found = False

        for card in self.p1.cards:
            if card.value == 9 and card.color == 0:
                if PRINT:
                    print('Player 1 is starting')
                nine_found = True

        if not nine_found:
            if PRINT:
                print("Player 2 starts")
            return self.p2

        return self.p1

    def list_pile(self):
        if PRINT:
            print("Cards on pile are")
            for card in self.card_pile:
              card.print()
            print('\n')

    def get_next_player(self, previous_player_id: int) -> Player:
        if previous_player_id == 1:
            return self.p2
        else:
            return self.p1

    def is_game_finished(self):
        if len(self.p1.cards) == 0 or len(self.p2.cards) == 0:
            return True
        return False

    def get_winner(self):
        if len(self.p1.cards) == 0:
            return self.p1
        else:
            return self.p2

    def get_looser(self):
        if len(self.p1.cards) == 0:
            return self.p2
        else:
            return self.p1
    # Return player that won

    def start_game(self):
        p1_victories = 0
        p2_victories = 0
        # self.p1 = pd.read_pickle('Agents/player_one')
        # self.create_new_game()
        first_time = datetime.now()
        number_of_draws = 0
        for i in range(20000):
            if i % 1000 == 0:
                print(p1_victories)
                print(p2_victories)
                second_time = datetime.now()
                print(str(i) + ", time: " + str((second_time - first_time).seconds))
                with open('player_one_lim', 'wb') as player_one_file:
                    pickle.dump(self.p1, player_one_file)
                with open('player_two_lim', 'wb') as player_two_file:
                    pickle.dump(self.p2, player_two_file)
                first_time = datetime.now()

            # print("*********START OF THE GAME*****************")
            starting_player = self.select_starting_player()
            starting_player.move(pile=self.card_pile, is_starting_move=True)
            self.p1.get_state()
            self.p2.get_state()
            self.list_pile()
            next_player = self.get_next_player(starting_player.id)
            number_of_moves = 0
            draw = False
            while not self.is_game_finished():
                if PRINT:
                    print(f"***************************** Player {next_player.id} move starts now *****************************")
                next_player.move(pile=self.card_pile)
                self.list_pile()
                next_player = self.get_next_player(next_player.id)
                number_of_moves += 1
                if number_of_moves > 5000:
                    draw = True
                    number_of_draws += 1
                    if number_of_draws % 100 == 0:
                        print(str(number_of_draws) + " draws")
                    break
            if draw:
                self.p1.update_graphs_after_result(False)
                self.p2.update_graphs_after_result(False)
            else:
                winner = self.get_winner()
                if winner.id == self.p1.id:
                    p1_victories += 1
                else:
                    p2_victories += 1
                winner.update_graphs_after_result(True)
                looser = self.get_looser()
                looser.update_graphs_after_result(False)
            # print(f"Game won by Player{winner.id}")
            self.create_new_game()
        print(p1_victories)
        print(p2_victories)
        # with open('player_one', 'rb') as player_one_file:
        #     pickle.dump(self.p1, player_one_file)
        # with open('player_two', 'rb') as player_two_file:
        #     pickle.dump(self.p2, player_two_file)
        print("THE END")
