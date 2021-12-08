
from scanner import Scanner, ReachedEOF
from statics import ERROR_FILE_PATH, KEYWORDS, SYMBOL_TABLE_FILE_PATH, TOKENS_FILE_PATH, INPUT_FILE_PATH, TokenNames

symbol_table = set(KEYWORDS)


def get_all_tokens():
    scanner = Scanner(errors_file_path=ERROR_FILE_PATH, tokens_file_path=TOKENS_FILE_PATH,
                      input_file_path=INPUT_FILE_PATH)
    while True:
        token_name, token_lexeme = scanner.get_next_token()
        if token_name is TokenNames.ID.name:
            symbol_table.add(token_lexeme)
        elif token_name is TokenNames.EOF.name:
            write_symbol_table_in_file()
            break



def write_symbol_table_in_file():
    result = ''
    for index, lexeme in enumerate(symbol_table):
        result += f'{index+1}.\t{lexeme}\n'
    SYMBOL_TABLE_FILE_PATH.write_text(result)


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
