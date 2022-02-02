from pathlib import Path
from code_generator import CodeGenerator
from parser_statics import PARSE_TREE_FILE_PATH, NonTerminalNames, EPSILON
from scanner import Scanner
from statics import TokenNames
from transition_diagram import State, NonTerminal
from typing import List, Union, Tuple, Any
from anytree import Node, RenderTree
from statics import KEYWORDS, SYMBOL_TABLE_FILE_PATH

# handle line number for EOF in normal state and unclosed comment error


class Parser:
    # stack, transition diagram, func next_state,
    def __init__(self, scanner: Scanner, syntax_errors_file_path: Path, code_generator: CodeGenerator):
        self.initialize_diagrams()
        self.scanner = scanner
        self.present_state = State.get_state_by_id(0)
        self.next_state_stack = []
        self.diagram = NonTerminal.get_nonterminal_by_name(
            NonTerminalNames.PROGRAM.value)
        self.diagram_stack = []
        self.parent_node = Node(self.diagram.name)
        self.parent_node_stack = []
        self.syntax_errors_file_path = syntax_errors_file_path
        self.symbol_table = []
        self.code_generator = code_generator
        self.code_generator.symbol_table = self.symbol_table
        self.action_symbol_stack = []

    def initialize_diagrams(self):
        State.create_all_states()
        NonTerminal.create_all_non_terminals()
        State.correct_references()
        NonTerminal.correct_relations()

    def run(self):
        self.set_next_token()
        self.reached_EOF = False
        while not self.reached_EOF:
            self.go_next_state()

    def set_next_token(self):
        self.token_name, self.token_lexeme, self.line_number = self.scanner.get_next_token()
        self.token_terminal_parameter = self.token_lexeme if self.token_name in {
            TokenNames.SYMBOL.value, TokenNames.KEYWORD.value, TokenNames.EOF.value} else self.token_name

    def find_path(self) -> Union[Tuple[Any, Any, Any], bool]:
        for edge, next_state, action_symbol in self.present_state.children:
            if self.is_valid_edge(edge):
                return edge, next_state, action_symbol
        return False

    def is_valid_edge(self, edge: Union[NonTerminal, str]) -> bool:
        if isinstance(edge, NonTerminal):
            return (self.token_terminal_parameter in edge.first) or (
                EPSILON in edge.first and self.token_terminal_parameter in edge.follow)
        else:
            return self.token_terminal_parameter == edge or (
                edge == EPSILON and self.token_terminal_parameter in self.diagram.follow)

    def go_next_state(self):
        # when present state is final state
        if self.present_state.is_final:
            if len(self.next_state_stack) == 0:
                return self.handle_EOF()
            else:
                self.present_state = self.next_state_stack.pop()
                self.diagram = self.diagram_stack.pop()
                self.parent_node = self.parent_node_stack.pop()
                if len(self.action_symbol_stack) > 0:
                    if self.action_symbol_stack[-1][2]:
                        self.code_generator.handle_action_symbol(
                            *self.action_symbol_stack.pop())
                return
        path = self.find_path()
        if not path:
            return self.handle_error()
        edge, next_state, action_symbol = path

        if isinstance(edge, NonTerminal):
            self.next_state_stack.append(next_state)
            self.present_state = edge.starting_state
            self.diagram_stack.append(self.diagram)
            self.diagram = edge
            self.parent_node_stack.append(self.parent_node)
            self.parent_node = Node(self.diagram.name, parent=self.parent_node)
            self.action_symbol_stack.append(
                [self.token_name, self.token_lexeme, action_symbol])
        else:
            if action_symbol:
                self.code_generator.handle_action_symbol(
                    self.token_name, self.token_lexeme, action_symbol)
            if edge == EPSILON:
                Node(EPSILON, parent=self.parent_node)
            else:
                if self.token_name == TokenNames.EOF.value:
                    Node(f'{self.token_lexeme}', parent=self.parent_node)
                else:
                    Node(f'({self.token_name}, {self.token_lexeme})',
                         parent=self.parent_node)
                self.set_next_token()
            self.present_state = next_state

    def handle_error(self):
        if self.token_name == TokenNames.EOF.value:
            error = f'#{self.line_number} : syntax error, Unexpected EOF\n'
            self.write_error_in_file(error)
            self.parent_node = self.parent_node_stack.pop(0)
            return self.handle_EOF()
        for edge, next_state, action_symbol in self.present_state.children:
            if isinstance(edge, NonTerminal) and self.token_terminal_parameter in edge.follow:
                error = f'#{self.line_number} : syntax error, missing {edge.name}\n'
                self.present_state = next_state
                return self.write_error_in_file(error)
            elif not isinstance(edge, NonTerminal) and edge != '$':
                error = f'#{self.line_number} : syntax error, missing {edge}\n'
                self.present_state = next_state
                return self.write_error_in_file(error)
        error = f'#{self.line_number} : syntax error, illegal {self.token_terminal_parameter}\n'
        self.write_error_in_file(error)
        return self.set_next_token()

    def handle_EOF(self):
        self.write_symbol_table_in_file()
        self.write_parse_tree_in_file()
        self.handle_empty_syntax_errors_file()
        self.reached_EOF = True

    def write_error_in_file(self, error: str):
        with open(self.syntax_errors_file_path, 'a') as syntax_errors_file:
            syntax_errors_file.write(error)

    def write_parse_tree_in_file(self):
        result = ''
        for pre, fill, node in RenderTree(self.parent_node):
            treestr = u"%s%s" % (pre, node.name)
            result += treestr.ljust(1) + '\n'
        PARSE_TREE_FILE_PATH.write_text(result, encoding='UTF-8')

    def write_symbol_table_in_file(self):
        result = ''
        for index, lexeme in enumerate(self.symbol_table):
            result += f'{index + 1}.\t{lexeme}\n'
        SYMBOL_TABLE_FILE_PATH.write_text(result)

    def handle_empty_syntax_errors_file(self):
        with open(self.syntax_errors_file_path, 'r+') as syntax_errors_file:
            if syntax_errors_file.read(1) == '':
                syntax_errors_file.write('There is no syntax error.')
