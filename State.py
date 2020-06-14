class State:
    def __init__(self, number_of_nines, number_of_tens, number_of_jacks, number_of_queens, number_of_kings,
                 number_of_aces, number_of_nines_on_pile, number_of_tens_on_pile, number_of_jacks_on_pile,
                 number_of_queens_on_pile, number_of_kings_on_pile, number_of_aces_on_pile):
        self.number_of_nines = number_of_nines
        self.number_of_tens = number_of_tens
        self.number_of_jacks = number_of_jacks
        self.number_of_queens = number_of_queens
        self.number_of_kings = number_of_kings
        self.number_of_aces = number_of_aces
        self.number_of_nines_on_pile = number_of_nines_on_pile
        self.number_of_tens_on_pile = number_of_tens_on_pile
        self.number_of_jacks_on_pile = number_of_jacks_on_pile
        self.number_of_queens_on_pile = number_of_queens_on_pile
        self.number_of_kings_on_pile = number_of_kings_on_pile
        self.number_of_aces_on_pile = number_of_aces_on_pile

    def __eq__(self, other):
        return self.number_of_nines == other.number_of_nines and self.number_of_tens == other.number_of_tens \
               and self.number_of_jacks == other.number_of_jacks and self.number_of_queens == other.number_of_queens \
               and self.number_of_kings == other.number_of_kings and self.number_of_aces == other.number_of_aces\
               and self.number_of_nines_on_pile == other.number_of_nines_on_pile \
               and self.number_of_tens_on_pile == other.number_of_tens_on_pile \
               and self.number_of_jacks_on_pile == other.number_of_jacks_on_pile \
               and self.number_of_queens_on_pile == other.number_of_queens_on_pile \
               and self.number_of_kings_on_pile == other.number_of_kings_on_pile \
               and self.number_of_aces_on_pile == other.number_of_aces_on_pile
