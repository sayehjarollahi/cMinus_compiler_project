import enum
from pathlib import Path

ERROR_FILE_PATH = Path('./lexical_errors.txt')
TOKENS_FILE_PATH = Path('./tokens.txt')
SYMBOL_TABLE_FILE_PATH = Path('./symbol_table.txt')
INPUT_FILE_PATH = Path('./input.txt')


class Regex(enum.Enum):
    SLASH = {'/'}
    DIGIT = set('0123456789')
    LETTER = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    SYMBOL = set(';:,[](){}+-*=<')
    WHITESPACE = {chr(32), chr(10), chr(13), chr(9), chr(11), chr(12)}
    EOF = {chr(5)}
    ALL_ALLOWED = DIGIT | LETTER | SYMBOL | WHITESPACE | EOF | SLASH
    NUM_OTHER = SYMBOL | WHITESPACE | EOF | SLASH
    LETTER_OR_DIGIT = DIGIT | LETTER
    ID_KEYWORD_OTHER = NUM_OTHER
    NOT_SLASH = ALL_ALLOWED - SLASH
    BACKSLASH = {'\\'}
    INSIDE_ONE_LINE_COMMENT = set(
        '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\r') | {chr(11)} | {chr(12)} | DIGIT | LETTER
    END_ONE_LINE_COMMENT = {chr(10), chr(5)}
    STAR = {'*'}
    NOT_STAR_EOF = set(
        '!"#$%&\'()+,-./:;<=>?@[\\]^_`{|}~ \t\n\r') | {chr(11)} | {chr(12)} | DIGIT | LETTER
    NOT_SLASH_STAR_EOF = NOT_STAR_EOF - SLASH
    EQUAL = {'='}
    SYMBOL_NOT_EQUAL = SYMBOL - EQUAL
    SYMBOL_OTHER = DIGIT | LETTER | SYMBOL_NOT_EQUAL | WHITESPACE | SLASH | EOF
    SYMBOL_NOT_STAR = SYMBOL - STAR
    END_LINE = {chr(10)}


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


IGNORING_TOKEN_NAMES = [TokenNames.WHITESPACE.name, TokenNames.COMMENT.name]


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

KEYWORDS = ['if', 'else', 'void', 'int',
            'repeat', 'break', 'until', 'return', 'endif']
