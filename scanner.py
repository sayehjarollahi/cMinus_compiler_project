from typing import List, Tuple, Optional
from pathlib import Path
from dfa import DFA, FinalState, InvalidInput, InvalidNumber, UnmatchedComment, UnclosedComment
from statics import TokenNames, KEYWORDS


class Scanner:

    def __init__(self, input_file_path: Path, tokens_file_path: Path, errors_file_path: Path,
                 symbol_table_file_path: Path):
        self.input_file = open(input_file_path, 'r')
        self.tokens_file_path = tokens_file_path
        self.errors_file_path = errors_file_path
        self.symbol_table_file_path = symbol_table_file_path
        self.keywords = KEYWORDS
        self.previous_character = ''
        self.current_character = self.input_file.read(1)
        self.current_lexeme = ''
        self.dfa = DFA()
        self.tokens = []
        self.error_messages = []
        self.symbol_table = []
        self.line_number = 1

    def get_next_token(self) -> Optional[Tuple[str, str]]:
        while True:
            if self.current_character == '':
                self.current_character = chr(5)
            try:
                self.dfa.move(self.current_character)
            except FinalState as final_state:
                if not final_state.retract_pointer:
                    self.move_pointer()
                if final_state.token_name == TokenNames.EOF.name:
                    self.write_line_in_files()
                    raise ReachedEOF()
                if final_state.token_name == TokenNames.ID_KEYWORD.name:
                    token = self.get_id_keyword_token()
                    self.add_token(token[0], token[1])
                    self.reset_lexem()
                    return token
                elif final_state.token_name == TokenNames.WHITESPACE.name:
                    if self.current_lexeme == '\n':
                        self.line_number += 1
                token = final_state.token_name, self.current_lexeme
                self.reset_lexem()
                self.add_token(token[0], token[1])
                return token
            except (InvalidInput, InvalidNumber, UnmatchedComment) as error_message:
                self.error_messages.append((self.current_lexeme, str(error_message)))
                self.reset_lexem()
                self.move_pointer()
            except UnclosedComment:
                self.append_unclosed_comment_lexeme()
                self.reset_lexem()
                self.write_line_in_files()
                raise ReachedEOF()
            else:
                self.move_pointer()

    def get_id_keyword_token(self):
        if self.current_lexeme in self.keywords:
            return TokenNames.KEYWORD.name, self.current_lexeme
        else:
            return TokenNames.ID.name, self.current_lexeme

    def append_unclosed_comment_lexeme(self):
        lexeme = self.current_lexeme
        if len(self.current_lexeme) > 7:
            lexeme = self.current_lexeme[0:6]
            lexeme += '...'
        self.error_messages.append((lexeme, 'Unclosed comment'))

    def move_pointer(self):
        self.current_lexeme = self.current_lexeme + self.current_character
        self.previous_character = self.current_character
        self.current_character = self.input_file.read(1)

    def write_line_in_files(self):
        if self.tokens:
            with self.tokens_file_path.open('a') as token_file:
                token_file.write(get_formatted_string(self.line_number, self.tokens))
            self.tokens = []
        if self.error_messages:
            with self.tokens_file_path.open('a') as error_file:
                error_file.write(get_formatted_string(self.line_number, self.error_messages))
            self.error_messages = []

    def add_token(self, token_name, token_lexeme):
        self.tokens.append((token_name, token_lexeme))

    def reset_lexem(self):
        self.current_lexeme = ''


def get_formatted_string(line_number: int, strings_list: List[str]) -> str:
    result = str(line_number)+'.\t'
    for item in strings_list:
        result = result + '('+ item[0] + ', '+item[1]+') '
    result += '\n'
    return result
    #return f'{line_number}.\t' + ('{} ' * len(strings_list).format(*strings_list)) + '\n'


class ReachedEOF(Exception):
    pass
