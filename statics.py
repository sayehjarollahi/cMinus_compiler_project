import enum


class Regex(enum.Enum):
    DIGIT = r'\d'
    LETTER = r'[A-Za-z]'
    SYMBOL = r'[;:,\[\]\(\){}\+\-\*=<]'
    WHITESPACE = r'[\x32\x10\x13\x09\x11\x12]'
    EOF = r'\x05'
    ALL_ALLOWED = DIGIT + '|' + LETTER + '|' + SYMBOL + '|' + '|' + WHITESPACE + '|' + EOF
    NUM_OTHER = SYMBOL + '|' + '|' + WHITESPACE + '|' + EOF
    LETTER_OR_DIGIT = DIGIT + '|' + LETTER
    ID_KEYWORD_OTHER = NUM_OTHER
    SLASH = r'/'
    NOT_BACKSLASH = r'[^\\]'
    BACKSLASH = r'\\'
    INSIDE_ONE_LINE_COMMENT = r'[^\x10\x05]'
    END_ONE_LINE_COMMENT = r'[\x10\x05]'
    STAR = r'\*'
    NOT_STAR = r'[^\*]'
    NOT_SLASH_STAR = r'[^/\*]'
    EQUAL = r'='
    SYMBOL_NOT_EQUAL = r'[;:,\[\]\(\){}\+\-\*<]'
    SYMBOL_OTHER = DIGIT + '|' + LETTER + '|' + SYMBOL_NOT_EQUAL + '|' + WHITESPACE
    SYMBOL_NOT_STAR = SYMBOL = r'[;:,\[\]\(\){}\+\-=<]'


class TokenNames(enum.Enum):
    SYMBOL = 'SYMBOL',
    NUM = 'NUM',
    ID = 'ID',
    KEYWORD = 'KEYWORD',
    COMMENT = 'COMMENT',
    WHITESPACE = 'WHITESPACE',
    ID_KEYWORD = 'ID_KEYWORD',
    INVALID_NUMBER = 'INVALID_NUMBER',
    UNMATCHED_COMMENT = 'UNMATCHED_COMMENT'


STATE0_TRANSITIONS = [
    (1, Regex.DIGIT),
    (3, Regex.LETTER),
    (5, Regex.SLASH),
    (11, Regex.WHITESPACE),
    (12, Regex.EQUAL),
    (15, Regex.SYMBOL_NOT_STAR),
    (16, Regex.STAR)
]

STATE1_TRANSITIONS = [
    (1, Regex.DIGIT),
    (2, Regex.NUM_OTHER),
    (18, Regex.LETTER)
]

STATE3_TRANSITIONS = [
    (3, Regex.LETTER_OR_DIGIT),
    (4, Regex.ID_KEYWORD_OTHER)
]

STATE5_TRANSITIONS = [
    (6, Regex.SLASH),
    (8, Regex.STAR)
]
STATE6_TRANSITIONS = [
    (6, Regex.INSIDE_ONE_LINE_COMMENT),
    (7, Regex.END_ONE_LINE_COMMENT)
]
STATE8_TRANSITIONS = [
    (8, Regex.NOT_STAR),
    (9, Regex.STAR)
]

STATE9_TRANSITIONS = [
    (9, Regex.STAR),
    (10, Regex.SLASH),
    (8, Regex.NOT_SLASH_STAR)
]

STATE12_TRANSITIONS = [
    (13, Regex.SYMBOL_OTHER),
    (14, Regex.EQUAL)
]
STATE16_TRANSITIONS = [
    (17, Regex.NOT_BACKSLASH),
    (18, Regex.BACKSLASH)
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
    11: (TokenNames.WHITESPACE.name, True),
    13: (TokenNames.SYMBOL, True),
    14: (TokenNames.SYMBOL, False),
    15: (TokenNames.SYMBOL, False),
    17: (TokenNames.SYMBOL, True),
    18: (TokenNames.INVALID_NUMBER, False),
    19: (TokenNames.UNMATCHED_COMMENT, False)
}
