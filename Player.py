from Card import Card


class Player:

    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)
