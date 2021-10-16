import enum


class FinalStates(enum.Enum):
    SYMBOL = (1,)
    NUM = (5, True)


class Regex(enum.Enum):
    ID_KEYWORD_OTHER = r'[^A-Za-z0-9]'


transitions = list()
transitions.append((0, 1, Regex.ID_KEYWORD_OTHER.value))

final_states = (1, 2, 3, 4, 5, 6, 7)
