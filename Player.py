from Card import Card, card_values
from Move import Move, ActionType
PRINT = False
inverted_card_values = {v: k for k, v in card_values.items()}


class Player:

    def __init__(self, id: int):
        self.cards = []
        self.id = id

    def add_card(self, card: Card):
        self.cards.append(card)

    def list_cards(self, show_colors):
        if PRINT:
            for card in self.cards:
                card.print(show_colors)
            print('\n')

    def move(self, pile: [Card], is_starting_move=False):
        if is_starting_move:
            self.throw_card(pile=pile, card_value=9, card_color=0)
        else:
            card_on_top = pile[-1]
            if PRINT:
                print(f"Card on top of pile = {card_on_top.string_value}")
                print("Your cards are")
            self.list_cards(show_colors=False)

            list_of_moves = self.list_possible_moves(pile=pile)
            if PRINT:
                print("Which move you want to make")
            move_to_make_id = int(input())
            move_to_make = next((m for m in list_of_moves if m.move_id == move_to_make_id), None)
            if PRINT:
                print(f"Executing move {move_to_make_id}")
            self.execute_move(move=move_to_make, pile=pile)

    def execute_move(self, move: Move, pile: [Card]):
        if move.action_type == ActionType.DRAW:
            self.draw_cards(pile, number_of_cards_to_draw=move.number_of_actionable_cards)
        elif move.action_type == ActionType.THROW:
            self.throw_card(pile=pile, card_value=inverted_card_values[move.card_value],
                            number_of_cards_to_throw=move.number_of_actionable_cards)

    def list_possible_moves(self, pile: [Card]) -> [Move]:
        occurrences = {}
        move_id = 0

        for card in self.cards:
            if card.string_value in occurrences:
                occurrences[card.string_value] += 1
            else:
                occurrences[card.string_value] = 1
        possible_moves = []

        if len(pile) > 1:
            number_of_cards_to_draw = 3
            if len(pile)-1 < number_of_cards_to_draw:
                number_of_cards_to_draw = len(pile)-1
            draw_move = Move(action_type=ActionType.DRAW, number_of_actionable_cards=number_of_cards_to_draw,
                             move_id=move_id)
            move_id += 1
            possible_moves.append(draw_move)

        for k, v in occurrences.items():
            if not self.can_throw_card_on_pile(card_value=inverted_card_values[k], pile=pile):
                continue
            if v >= 1:
                # throw one card
                move = Move(action_type=ActionType.THROW, number_of_actionable_cards=1, card_value=k, move_id=move_id)
                move_id += 1
                possible_moves.append(move)
            if v >= 3:
                # throw three cards
                move = Move(action_type=ActionType.THROW, number_of_actionable_cards=3, card_value=k, move_id=move_id)
                move_id += 1
                possible_moves.append(move)
            if v == 4:
                move = Move(action_type=ActionType.THROW, number_of_actionable_cards=4, card_value=k, move_id=move_id)
                move_id += 1
                possible_moves.append(move)

        for move in possible_moves:
            move.print()

        return possible_moves

    def can_throw_card_on_pile(self, card_value: int, pile: [Card]) -> bool:
        card_on_top = pile[-1]
        if card_value >= card_on_top.value:
            return True
        return False

    def draw_cards(self, pile: [Card], number_of_cards_to_draw):
        for i in range(0, number_of_cards_to_draw):
            card_to_draw = pile.pop()
            self.cards.append(card_to_draw)

    def throw_card(self, pile: [], card_value: int, number_of_cards_to_throw: int = None, card_color: int = None):
        if card_color is not None:
            card_to_throw = Card(color=card_color, value=card_value)
            player_card = next((card for card in self.cards if
                                card.value == card_to_throw.value and card_to_throw.color == card.color))
            pile.append(player_card)
            self.cards.remove(player_card)
            if PRINT:
                print(f"Player {self.id} thrown {player_card.color}|{player_card.value} onto the pile")

        else:
            for i in range(0, number_of_cards_to_throw):
                for card in self.cards:
                    if card.value == card_value:
                        pile.append(card)
                        card_to_remove = card
                        self.cards.remove(card_to_remove)
                        if PRINT:
                            print(f"Player {self.id} thrown {card_to_remove.color}|{card_to_remove.value} onto the pile")
                        break
