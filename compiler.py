import re
from pathlib import Path

from scanner import Scanner, ReachedEOF
from statics import Regex

ERROR_FILE_PATH = Path('./lexical_errors.txt')
TOKENS_FILE_PATH = Path('./tokens.txt')
SYMBOL_TABLE_FILE_PATH = Path('./symbol_table.txt')
INPUT_FILE_PATH = Path('./input.txt')


def get_all_tokens():
    scanner = Scanner(errors_file_path=ERROR_FILE_PATH, tokens_file_path=TOKENS_FILE_PATH, input_file_path=INPUT_FILE_PATH, symbol_table_file_path=SYMBOL_TABLE_FILE_PATH)
    while True:
        try:
            token_name, token_lexeme = scanner.get_next_token()
           # print(str(scanner.line_number)+' '+token_name+'{' +token_lexeme+'}')
        except ReachedEOF:
            break


open(ERROR_FILE_PATH, 'w')
open(TOKENS_FILE_PATH, 'w')
open(SYMBOL_TABLE_FILE_PATH, 'w')
get_all_tokens()

# file = open(INPUT_FILE_PATH,'r')
# line=0
# while True:
#     next = file.read(1)
#     line+=1
#     if re.match(Regex.WHITESPACE.value,next):
#         print(line,'hi')
#
#     if next =='':
#         break