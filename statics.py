import enum
from pathlib import Path

ERROR_FILE_PATH = Path('./lexical_errors.txt')
TOKENS_FILE_PATH = Path('./tokens.txt')
SYMBOL_TABLE_FILE_PATH = Path('./symbol_table.txt')
INPUT_FILE_PATH = Path('./input.txt')


class Regex(enum.Enum):
    SLASH = r'/'
    DIGIT = r'\d'
    LETTER = r'[A-Za-z]'
    SYMBOL = r'[;:,\[\]\(\){}\+\-\*=<]'
    WHITESPACE = r'[\x20\x0a\x0d\x09\x0b\x0c ]'
    EOF = r'\x05'
    ALL_ALLOWED = DIGIT + '|' + LETTER + '|' + SYMBOL + '|' + WHITESPACE + '|' + EOF + '|' + '/'
    NUM_OTHER = SYMBOL + '|' + WHITESPACE + '|' + EOF + '|'+SLASH
    LETTER_OR_DIGIT = DIGIT + '|' + LETTER
    ID_KEYWORD_OTHER = NUM_OTHER
    NOT_SLASH = r'[^/]'
    BACKSLASH = r'\\'
    INSIDE_ONE_LINE_COMMENT = r'[^\x0a\x05]'
    END_ONE_LINE_COMMENT = r'[\x0a\x05]'
    STAR = r'\*'
    NOT_STAR_EOF = r'[^\*\x05]'
    NOT_SLASH_STAR_EOF = r'[^/\*\x05]'
    EQUAL = r'='
    SYMBOL_NOT_EQUAL = r'[;:,\[\]\(\){}\+\-\*<]'
    SYMBOL_OTHER = DIGIT + '|' + LETTER + '|' + SYMBOL_NOT_EQUAL + '|' + WHITESPACE + '|'+SLASH
    SYMBOL_NOT_STAR = r'[;:,\[\]\(\){}\+\-=<]'
    END_LINE = r'\x0a'


class TokenNames(enum.Enum):
    SYMBOL = 'SYMBOL'
    NUM = 'NUM'
    ID = 'ID'
    KEYWORD = 'KEYWORD'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    ID_KEYWORD = 'ID_KEYWORD'
    UNMATCHED_COMMENT = 'UNMATCHED_COMMENT'
    EOF = 'EOF'


STATE0_TRANSITIONS = [
    (1, Regex.DIGIT.value),
    (3, Regex.LETTER.value),
    (5, Regex.SLASH.value),
    (11, Regex.WHITESPACE.value),
    (12, Regex.EQUAL.value),
    (15, Regex.SYMBOL_NOT_STAR.value),
    (16, Regex.STAR.value),
    (18, Regex.EOF.value)
]

STATE1_TRANSITIONS = [
    (1, Regex.DIGIT.value),
    (2, Regex.NUM_OTHER.value)
]

STATE3_TRANSITIONS = [
    (3, Regex.LETTER_OR_DIGIT.value),
    (4, Regex.ID_KEYWORD_OTHER.value)
]

STATE5_TRANSITIONS = [
    (6, Regex.SLASH.value),
    (8, Regex.STAR.value)
]
STATE6_TRANSITIONS = [
    (6, Regex.INSIDE_ONE_LINE_COMMENT.value),
    (7, Regex.END_ONE_LINE_COMMENT.value)
]
STATE8_TRANSITIONS = [
    (8, Regex.NOT_STAR_EOF.value),
    (9, Regex.STAR.value)
]

STATE9_TRANSITIONS = [
    (9, Regex.STAR.value),
    (10, Regex.SLASH.value),
    (8, Regex.NOT_SLASH_STAR_EOF.value)
]

STATE12_TRANSITIONS = [
    (13, Regex.SYMBOL_OTHER.value),
    (14, Regex.EQUAL.value)
]
STATE16_TRANSITIONS = [
    (17, Regex.NOT_SLASH.value),
]
TRANSITIONS = {
    0: STATE0_TRANSITIONS,
    1: STATE1_TRANSITIONS,
    3: STATE3_TRANSITIONS,
    5: STATE5_TRANSITIONS,
    6: STATE6_TRANSITIONS,
    8: STATE8_TRANSITIONS,
    9: STATE9_TRANSITIONS,
    12: STATE12_TRANSITIONS,
    16: STATE16_TRANSITIONS

}

FINAL_STATES = {
    2: (TokenNames.NUM.name, True),
    4: (TokenNames.ID_KEYWORD.name, True),
    7: (TokenNames.COMMENT.name, True),
    10: (TokenNames.COMMENT.name, False),
    11: (TokenNames.WHITESPACE.name, False),
    13: (TokenNames.SYMBOL.name, True),
    14: (TokenNames.SYMBOL.name, False),
    15: (TokenNames.SYMBOL.name, False),
    17: (TokenNames.SYMBOL.name, True),
    18: (TokenNames.EOF.name, False)
}

KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
