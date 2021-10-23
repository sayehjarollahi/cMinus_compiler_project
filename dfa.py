import re
from statics import Regex, TRANSITIONS, FINAL_STATES


class DFA:
    """
    param transitions_dict: state_number: list[next_state, regex for transition between states]
    param final_states: final_state_number: token_name, retract_pointer boolean
    """

    def __init__(self):
        self.transitions_dict = TRANSITIONS
        self.final_states = FINAL_STATES
        self.current_state = 0

    def move(self, current_char: str):
        if not re.match(Regex.ALL_ALLOWED.value, current_char):
            raise InvalidInput('Invalid input')
        for next_state, regex in self.transitions_dict.get(self.current_state, []):
            if re.match(regex, current_char):
                self.current_state = next_state
                self.handle_final_state()
                break
            else:
                if self.current_state == 1:
                    self.current_state = 0
                    raise InvalidNumber('Invalid number')
                elif self.current_state == 16:
                    self.current_state = 0
                    raise UnmatchedComment('Unmatched comment')
                elif self.current_state == 8 or self.current_state == 9:
                    self.current_state = 0
                    raise UnclosedComment()
                elif self.current_state == 5:
                    self.current_state = 0
                    raise InvalidInput('Invalid input')

    def handle_final_state(self):
        if self.current_state in self.final_states:
            final_state_number = self.current_state
            self.current_state = 0
            raise FinalState(*self.final_states[final_state_number])


class FinalState(Exception):
    def __init__(self, token_name: str, retract_pointer: bool):
        self.token_name = token_name
        self.retract_pointer = retract_pointer


class CannotMove(Exception):
    pass


class InvalidInput(CannotMove):
    pass


class InvalidNumber(CannotMove):
    pass


class UnmatchedComment(CannotMove):
    pass


class UnclosedComment(Exception):
    pass
