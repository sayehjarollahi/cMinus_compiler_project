import re
from typing import List, Tuple, Optional
from pathlib import Path
from dfa import DFA, FinalState, InvalidInput, InvalidNumber, UnmatchedComment


class Scanner:

    def __init__(self, input_file_path: Path, tokens_file_path: Path, errors_file_path: Path, symbol_table_file_path: Path, keywords: List[str], dfa: DFA):
        self.line = 1
        self.input_file = open(input_file_path, 'r')
        self.tokens_file_path = tokens_file_path
        self.errors_file_path = errors_file_path
        self.symbol_table_file_path = symbol_table_file_path
        self.keywords = keywords
        self.previous_character = ''
        self.current_character = self.input_file.read(1)
        self.current_lexeme = ''
        self.dfa = dfa
        self.tokens = []
        self.error_messages = []
        self.symbol_table = []

    def get_next_token(self) -> Optional[Tuple[str, str]]:
        '''abcd=h
        self.current_character = read_char
        self.token = self.token + self.current_character
        move
        '''
        while True:
            try:
                self.dfa.move(self.current_character)
            except FinalState as final_state:
                if not final_state.retract_pointer:
                    self.move_pointer()
                if final_state.token_name == 'NUM' or final_state.token_name == 'SYMBOL':
                    return final_state.token_name, self.current_lexeme
                if final_state.token_name == 'ID_KEYWORD':
                    if self.current_lexeme in self.keywords:
                        return 'KEYWORD', self.current_lexeme
                    else:
                        return 'ID', self.current_lexeme
                return
            except (InvalidInput, InvalidNumber, UnmatchedComment) as error_message:
                self.move_pointer()
                self.error_messages.append(
                    (self.current_lexeme, str(error_message)))
                return
            else:
                self.move_pointer()

    def move_pointer(self):
        self.current_lexeme = self.current_lexeme + self.current_character
        self.previous_character = self.current_character
        self.current_character = self.input_file.read(1)

    def write_in_files(self):
        if self.tokens:
            self.tokens_file_path.write_text(
                get_formatted_string(self.line, self.tokens), 'a')
            self.tokens = []
            if self.error_messages:
                self.errors_file_path.write_text(
                    get_formatted_string(self.line, self.error_messages), 'a')
                self.error_messages = []


def get_formatted_string(line_number: int, strings_list: List[str]) -> str:
    return f'{line_number}.\t' + ('{} '*len(strings_list).format(*strings_list)) + '\n'
