from typing import Tuple


class Scanner:

    def __init__(self, file_path):
        self.line = 0
        self.file = open(file_path, 'r')
        self.previous_character = 'd'
        self.current_character = '='
        self.current_token = 'abcd'


    def get_next_token(self) -> Tuple[str, str]:

        '''abcd=h
         self.current_character = read_char
        self.token = self.token + self.current_character
         move
         '''



