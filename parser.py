from scanner import Scanner
from transition_diagram import EPSILON, Node, NonTerminal
from typing import List, Union


class Parser:
    # stack, transition diagram, func next_state,
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.present_state = 0
        self.next_state_stack = []

    def set_next_token(self):
        self.token_name, self.token_lexeme, self.line_number = self.scanner.get_next_token()

    def find_path(self) -> Union[List[Union[NonTerminal, Node]], bool]:
        for edge, next_node in self.present_state.children():
            if self.is_next_node(edge):
                return edge, next_node
        return False

    def is_next_node(self, edge: Union[NonTerminal, str]) -> bool:
        if isinstance(edge, NonTerminal):
            return (self.token_lexeme in edge.first) or (EPSILON in edge.first and self.token_lexeme in edge.follow)
        else:
            return self.token_lexeme == edge

    def go_next_state(self):
        if not self.find_path():
            return self.handle_error()
        edge, next_state = self.find_path()
        if isinstance(edge, NonTerminal):
            add_anytree(edge)
            self.next_state_stack.append(next_state)
            self.present_state = edge.starting_node
        else:
            add_anytree(edge)
            self.set_next_token()
            self.present_state = next_state

    def handle_error(self):
        for edge, next_node in self.present_state.children():
            if isinstance(edge, NonTerminal):

    '''def next_state:
        for state, edge in neighbor_states[self.state]:
            if token in first(edge):
                return edge, state
            elif epsilon in first(edge):
                if next_state(state):
                    return edge, state  #queue
        return False'''
    # def handle_error()
