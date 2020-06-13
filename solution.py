from Card import Card, card_values
from pprint import pprint

amount_of_cards = 24
number_of_players = 2
number_of_card_colors = 4


def create_deck_of_cards() -> [Card]:

    deck = []

    for i in range(0, number_of_card_colors):
        for value in card_values.keys():
            card = Card(value=value, color=i)
            deck.append(card)
    return deck


deck = create_deck_of_cards()

for card in deck:
    card.print()
