from typing import Dict, Tuple, List, Union
import re


class DFA:

    def __init__(self, transitions: Dict[int, List[Tuple[int, str]]], final_states: Dict[int, Tuple[str, bool]]):
        '''

        :param transitions: state_number: list[next_state, regex for transition between states]
        param final_states: final_state_number: token_name, retract_pointer boolean
        '''
        self.transition_dict = transitions
        self.final_states = final_states
        self.current_state = 0

    def move(self, current_char: str) -> None:
        for next_state, regex in self.transition_dict.get(self.current_state, []):
            if re.match(regex, current_char):
                self.current_state = next_state
                if self.current_state in self.final_states:
                    raise FinalState(*self.final_states[self.current_state])
        else:
            raise CannotMove()


class FinalState(Exception):

    def __init__(self, token_name: str, retract_pointer: bool):
        self.token_name = token_name
        self.retract = retract_pointer


class CannotMove(Exception):
    pass
