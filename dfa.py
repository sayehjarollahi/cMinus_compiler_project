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
        self.new_line_counter = 0

    def move(self, current_char: str):
        if not re.match(Regex.ALL_ALLOWED.value, current_char) and self.current_state not in (1, 6, 8, 9):
            self.current_state = 0
            raise InvalidInput(False)
        for next_state, regex in self.transitions_dict.get(self.current_state, []):
            if re.match(regex, current_char):
                self.current_state = next_state
                if re.match(Regex.END_LINE.value, current_char) and self.current_state in (8, 11):
                    self.new_line_counter += 1
                self.handle_final_state()
                break
        else:
            if self.current_state == 1:
                self.current_state = 0
                raise InvalidNumber()
            elif self.current_state == 16:
                self.current_state = 0
                raise UnmatchedComment()
            elif self.current_state == 8 or self.current_state == 9:
                self.new_line_counter = 0
                self.current_state = 0
                raise UnclosedComment()
            elif self.current_state == 5:
                self.current_state = 0
                raise InvalidInput(True)

    def handle_final_state(self):
        if self.current_state in self.final_states:
            final_state_number = self.current_state
            self.current_state = 0
            new_line_counter = self.new_line_counter
            self.new_line_counter = 0
            raise FinalState(
                *self.final_states[final_state_number], new_line_counter)


class FinalState(Exception):
    def __init__(self, token_name: str, retract_pointer: bool, new_line_counter: int):
        self.token_name = token_name
        self.retract_pointer = retract_pointer
        self.new_line_counter = new_line_counter


class CannotMove(Exception):
    pass


class InvalidInput(CannotMove):
    def __init__(self, does_retract_pointer):
        self.does_retract_pointer = does_retract_pointer

    def __str__(self):
        return "Invalid input"


class InvalidNumber(CannotMove):

    def __str__(self):
        return "Invalid number"


class UnmatchedComment(CannotMove):
    def __str__(self):
        return "Unmatched comment"


class UnclosedComment(Exception):
    pass
