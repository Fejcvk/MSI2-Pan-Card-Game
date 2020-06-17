from enum import Enum
PRINT = False


class ActionType(Enum):
    DRAW = 0
    THROW = 1


class Move:
    def __init__(self, action_type: ActionType, move_id: int, number_of_actionable_cards=0, card_value=None):
        self.move_id = move_id
        self.action_type = action_type
        self.card_value = card_value
        self.number_of_actionable_cards = number_of_actionable_cards

    def print(self):
        if PRINT:
            print(
                f"{self.move_id}.Move kind {self.action_type}, number of actionable cards = {self.number_of_actionable_cards}, actionable card value = {self.card_value}")

