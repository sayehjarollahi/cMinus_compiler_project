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



transitions = list()
transitions.append((0, 1, Regex.ID_KEYWORD_OTHER.value))

final_states = (1, 2, 3, 4, 5, 6, 7)
