from pathlib import Path
from parser import Parser
from scanner import Scanner, ReachedEOF
from statics import ERROR_FILE_PATH, SYMBOL_TABLE_FILE_PATH, TOKENS_FILE_PATH, INPUT_FILE_PATH, TokenNames
from parser_statics import SYNTAX_ERRORS_FILE_PATH


scanner = Scanner(errors_file_path=ERROR_FILE_PATH, tokens_file_path=TOKENS_FILE_PATH,
                  input_file_path=INPUT_FILE_PATH)
parser = Parser(SYNTAX_ERRORS_FILE_PATH, scanner)
open(ERROR_FILE_PATH, 'w')
open(TOKENS_FILE_PATH, 'w')
open(SYMBOL_TABLE_FILE_PATH, 'w')


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
