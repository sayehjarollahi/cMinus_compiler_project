from pathlib import Path
from parser_statics import NonTerminalNames
from scanner import Scanner
from statics import TokenNames
from transition_diagram import EPSILON, Node, NonTerminal
from typing import List, Union
from anytree import Node, RenderTree


class Parser:
    # stack, transition diagram, func next_state,
    def __init__(self, scanner: Scanner, syntax_errors_file_path: Path):
        self.scanner = scanner
        self.present_state = Node.get_node_by_id(0)
        self.next_state_stack = []
        self.diagram = NonTerminal.get_nonterminal_by_name(
            NonTerminalNames.PROGRAM.value)
        self.diagram_stack = []
        self.parent_node = Node(self.diagram.name)
        self.parent_node_stack = []
        self.syntax_errors_file_path = syntax_errors_file_path

    def set_next_token(self):
        self.token_name, self.token_lexeme, self.line_number = self.scanner.get_next_token()
        self.token_terminal_parameter = self.token_lexeme if self.token_name in {
            TokenNames.SYMBOL.value, TokenNames.KEYWORD.value} else self.token_name

    def find_path(self) -> Union[List[Union[NonTerminal, Node]], bool]:
        for edge, next_state in self.present_state.children():
            if self.is_next_state(edge):
                return edge, next_state
        return False

    def is_next_state(self, edge: Union[NonTerminal, str]) -> bool:
        if isinstance(edge, NonTerminal):
            return (self.token_terminal_parameter in edge.first) or (EPSILON in edge.first and self.token_terminal_parameter in edge.follow)
        else:
            return self.token_terminal_parameter == edge or (edge == EPSILON and self.token_terminal_parameter in self.diagram.follow)

    def go_next_state(self):
        # when present state is final state
        if self.present_state.is_final:
            if len(self.next_state_stack) == 0:
                return self.handle_end_parser()
            else:
                self.present_state = self.next_state_stack.pop()
                self.diagram = self.diagram_stack.pop()
                self.parent_node = self.parent_node_stack.pop()
                return
        path = self.find_path()
        if not path:
            return self.handle_error()
        edge, next_state = path
        if isinstance(edge, NonTerminal):
            self.next_state_stack.append(next_state)
            self.present_state = edge.starting_node
            self.diagram_stack.append(self.diagram)
            self.diagram = edge
            self.parent_node_stack.append(self.parent_node)
            self.parent_node = Node(self.diagram.name, parent=self.parent_node)
        else:
            Node(f'({self.token_name}, {self.token_lexeme})',
                 parent=self.parent_node)
            self.set_next_token()
            self.present_state = next_state

    def handle_error(self):
        for edge, next_state in self.present_state.children():
            # handle EOF
            if isinstance(edge, NonTerminal):
                if self.token_terminal_parameter in edge.follow:
                    error = f'#{self.line_number} : syntax error, missing {edge.name}'
                    self.present_state = next_state
                    return self.write_error_in_file(error)
                else:
                    error = f'#{self.line_number} : syntax error, illegal {self.token_terminal_parameter}'
                    return self.set_next_token()
            else:
                error = f'#{self.line_number} : syntax error, missing {edge}'
                self.present_state = next_state
                return self.write_error_in_file(error)

    def handle_end_parser(self):
        pass

    def write_error_in_file(self, error: str):
        with open(self.syntax_errors_file_path, 'a') as syntax_errors_file:
            syntax_errors_file.write(error)

    def print_tree(self):
        for pre, fill, node in RenderTree(self.parent_node):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8))

    '''def next_state:
        for state, edge in neighbor_states[self.state]:
            if token in first(edge):
                return edge, state
            elif epsilon in first(edge):
                if next_state(state):
                    return edge, state  #queue
        return False'''
