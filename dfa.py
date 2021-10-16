from typing import Tuple, List


class DFA:

    def __init__(self, transitions: List[Tuple[int, int, str]], final_states: set):
        '''

        :param transitions: first_state , final_state, regex for transition between states
        '''
        self.transitions = transitions
        self.final_states = final_states
        self.current_state = 0

    def move(self, current_char: str) -> int:
        for transition in self.transitions:
            pass
        return 0


class FinalState(Exception):

    def __init__(self, state_number: int, ):
        pass


class MiddleState(Exception):
    pass

class CannotMove(Exception):
    pass


