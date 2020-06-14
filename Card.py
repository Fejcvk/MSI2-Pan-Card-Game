card_values = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: '10', 9: '9'}
card_colors = {0: 'H', 1: 'S', 2: 'D', 3: 'C'}

PRINT = False

class Card:

    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.string_value = card_values[self.value]

    def print(self, show_colors=True):
        if PRINT:
            if show_colors:
                print(f"{card_colors.get(self.color)}|{card_values.get(self.value)}", end=' ')
            else:
                print(f"{card_values.get(self.value)}", end=' ')
