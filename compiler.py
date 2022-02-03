from pathlib import Path

from code_generator import CodeGenerator
from parser_file import Parser
from scanner import Scanner
from statics import ERROR_FILE_PATH, SYMBOL_TABLE_FILE_PATH, TOKENS_FILE_PATH, INPUT_FILE_PATH
from parser_statics import SYNTAX_ERRORS_FILE_PATH, PARSE_TREE_FILE_PATH


scanner = Scanner(errors_file_path=ERROR_FILE_PATH, tokens_file_path=TOKENS_FILE_PATH,
                  input_file_path=INPUT_FILE_PATH)
code_generator = CodeGenerator()
parser = Parser(
    syntax_errors_file_path=SYNTAX_ERRORS_FILE_PATH, scanner=scanner, code_generator=code_generator)

open(ERROR_FILE_PATH, 'w')
open(TOKENS_FILE_PATH, 'w')
open(SYMBOL_TABLE_FILE_PATH, 'w')
open(SYNTAX_ERRORS_FILE_PATH, 'w')
open(PARSE_TREE_FILE_PATH, 'w')
parser.run()
