from enum import Enum
from pathlib import Path
from transition_diagram import NonTerminal

EPSILON = 'epsilon'
SYNTAX_ERRORS_FILE_PATH = Path('syntax_errors.txt')
PARSE_TREE_FILE_PATH = Path('parse_tree.txt')


class NonTerminalNames(Enum):
    PROGRAM = 'Program'
    DECLARATION_LIST = 'Declaration-list'
    DECLARATION = 'Declaration'
    DECLARATION_INITIAL = 'Declaration-initial'
    DECLARATION_PRIME = 'Declaration-prime'
    VAR_DECLARATION_PRIME = 'Var-declaration-prime'
    FUN_DECLARATION_PRIME = 'Fun-declaration-prime'
    TYPE_SPECIFIER = 'Type-specifier'
    PARAMS = 'Params'
    PARAM_LIST = 'Param-list'
    PARAM = 'Param'
    PARAM_PRIME = 'Param-prime'
    COMPOUND_STMT = 'Compound-stmt'
    STATEMENT_LIST = 'Statement-list'
    STATEMENT = 'Statement'
    EXPRESSION_STMT = 'Expression-stmt'
    SELECTION_STMT = 'Selection-stmt'
    ELSE_STMT = 'Else-stmt'
    ITERATION_STMT = 'Iteration-stmt'
    RETURN_STMT = 'Return-stmt'
    RETURN_STMT_PRIME = 'Return-stmt-prime'
    EXPRESSION = 'Expression'
    B = 'B'
    H = 'H'
    SIMPLE_EXPRESSION_ZEGOND = 'Simple-expression-zegond'
    SIMPLE_EXPRESSION_PRIME = 'Simple-expression-prime'
    C = 'C'
    RELOP = 'Relop'
    ADDITIVE_EXPRESSION = 'Additive-expression'
    ADDITIVE_EXPRESSION_PRIME = 'Additive-expression-prime'
    ADDITIVE_EXPRESSION_ZEGOND = 'Additive-expression-zegond'
    D = 'D'
    ADDOP = 'Addop'
    TERM = 'Term'
    TERM_PRIME = 'Term-prime'
    TERM_ZEGOND = 'Term-zegond'
    G = 'G'
    FACTOR = 'Factor'
    VAR_CALL_PRIME = 'Var-call-prime'
    VAR_PRIME = 'Var-prime'
    FACTOR_PRIME = 'Factor-prime'
    FACTOR_ZEGOND = 'Factor-zegond'
    ARGS = 'Args'
    ARG_LIST = 'Arg-list'
    ARG_LIST_PRIME = 'Arg-list-prime'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


# name, first, follow, starting node id
NON_TERMINALS = [
    (NonTerminalNames.PROGRAM, ['$', 'int', 'void'], ['$'], 0),
    (NonTerminalNames.DECLARATION_LIST, [EPSILON, 'int', 'void'],
     ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], 3),
    (NonTerminalNames.DECLARATION, ['int', 'void'],
     ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], 6),
    (NonTerminalNames.DECLARATION_INITIAL, [
     'int', 'void'], ['(', '[', ';', ',', ')'], 9),
    (NonTerminalNames.DECLARATION_PRIME, ['(', '[', ';'],
     ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], 12),
    (NonTerminalNames.VAR_DECLARATION_PRIME, ['[', ';'],
     ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'], 14),
    (NonTerminalNames.FUN_DECLARATION_PRIME, ['(', ],
     ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', ], 19),
    (NonTerminalNames.TYPE_SPECIFIER, ['int', 'void', ], ['ID', ], 24),
    (NonTerminalNames.PARAMS, ['int', 'void', ], [')', ], 26),
    (NonTerminalNames.PARAM_LIST, [',', EPSILON, ], [')', ], 31),
    (NonTerminalNames.PARAM, ['int', 'void', ], [',', ')'], 35),
    (NonTerminalNames.PARAM_PRIME, ['[', EPSILON, ], [',', ')'], 38),
    (NonTerminalNames.COMPOUND_STMT, ['{', ],
     ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else',
      'until', ], 41),
    (NonTerminalNames.STATEMENT_LIST, [EPSILON, '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', ], ['}'],
     46),
    (NonTerminalNames.STATEMENT, ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', ],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 49),
    (NonTerminalNames.EXPRESSION_STMT, ['break', ';', 'ID', '(', 'NUM', ],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 51),
    (NonTerminalNames.SELECTION_STMT, ['if', ],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 55),
    (NonTerminalNames.ELSE_STMT, ['endif', 'else'],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 62),
    (NonTerminalNames.ITERATION_STMT, ['repeat'],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 66),
    (NonTerminalNames.RETURN_STMT, ['return', ],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 73),
    (NonTerminalNames.RETURN_STMT_PRIME, [';', 'ID', '(', 'NUM', ],
     ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until', ], 76),
    (NonTerminalNames.EXPRESSION, [
     'ID', '(', 'NUM', ], [';', ')', ']', ',', ], 79),
    (NonTerminalNames.B, ['=', '[', '(', '*', '+', '-',
     '<', '==', EPSILON, ], [';', ')', ']', ',', ], 82),
    (NonTerminalNames.H, ['=', '*', EPSILON, '+',
     '-', '<', '==', ], [';', ')', ']', ',', ], 88),
    (NonTerminalNames.SIMPLE_EXPRESSION_ZEGOND, [
     '(', 'NUM', ], [';', ')', ']', ',', ], 93),
    (NonTerminalNames.SIMPLE_EXPRESSION_PRIME, [
     '(', '*', '+', '-', '<', '==', EPSILON, ], [';', ')', ']', ',', ], 96),
    (NonTerminalNames.C, [EPSILON, '<', '==', ], [';', ')', ']', ',', ], 99),
    (NonTerminalNames.RELOP, ['<', '==', ], ['(', 'ID', 'NUM', ], 102),
    (NonTerminalNames.ADDITIVE_EXPRESSION, [
     '(', 'ID', 'NUM', ], [';', ')', ']', ',', ], 104),
    (NonTerminalNames.ADDITIVE_EXPRESSION_PRIME, ['(', '*', '+', '-', EPSILON, ], ['<', '==', ';', ')', ']', ',', ],
     107),
    (NonTerminalNames.ADDITIVE_EXPRESSION_ZEGOND, [
     '(', 'NUM', ], ['<', '==', ';', ')', ']', ',', ], 110),
    (NonTerminalNames.D, [EPSILON, '+', '-', ],
     ['*', '<', '==', ';', ')', ']', ',', ], 113),
    (NonTerminalNames.ADDOP, ['+', '-', ], ['(', 'ID', 'NUM', ], 117),
    (NonTerminalNames.TERM, ['(', 'ID', 'NUM', ], [
     '+', '-', ';', ')', '*', '<', '==', ']', ',', ], 119),
    (NonTerminalNames.TERM_PRIME, [
     '(', '*', EPSILON, ], ['+', '-', '<', '==', ';', ')', ']', ',', ], 122),
    (NonTerminalNames.TERM_ZEGOND, ['(', 'NUM', ], [
     '+', '-', '<', '==', ';', ')', ']', ',', ], 125),
    (NonTerminalNames.G, ['*', EPSILON, ],
     ['<', '==', ';', ')', '+', '-', '*', ']', ',', ], 128),
    (NonTerminalNames.FACTOR, ['(', 'ID', 'NUM', ], [
     '*', '+', '-', ';', ')', '<', '==', ']', ',', ], 132),
    (NonTerminalNames.VAR_CALL_PRIME, [
     '(', '[', EPSILON, ], ['*', '+', '-', ';', ')', '<', '==', ']', ',', ], 137),
    (NonTerminalNames.VAR_PRIME, ['[', EPSILON, ], [
     '*', '+', '-', ';', ')', '<', '==', ']', ',', ], 141),
    (NonTerminalNames.FACTOR_PRIME, ['(', EPSILON, ], [
     '*', '+', '-', '<', '==', ';', ')', ']', ',', ], 145),
    (NonTerminalNames.FACTOR_ZEGOND, ['(', 'NUM', ], [
     '*', '+', '-', '<', '==', ';', ')', ']', ',', ], 149),
    (NonTerminalNames.ARGS, [EPSILON, 'ID', '(', 'NUM', ], [')', ], 153),
    (NonTerminalNames.ARG_LIST, ['ID', '(', 'NUM', ], [')', ], 155),
    (NonTerminalNames.ARG_LIST_PRIME, [',', EPSILON, ], [')', ], 158),
]

ALL_NODES = [
    (0, False, [[NonTerminalNames.DECLARATION_LIST, 1], ]),
    (1, False, [['$', 2], ]),
    (2, True, []),
    (3, False, [[NonTerminalNames.DECLARATION, 4], [EPSILON, 5]]),
    (4, False, [[NonTerminalNames.DECLARATION_LIST, 5]]),
    (5, True, []),
    (6, False, [[NonTerminalNames.DECLARATION_INITIAL, 7]]),
    (7, False, [[NonTerminalNames.DECLARATION_PRIME, 8]]),
    (8, True, []),
    (9, False, [[NonTerminalNames.TYPE_SPECIFIER, 10]]),
    (10, False, [['ID', 11]]),
    (11, True, []),
    (12, False, [[NonTerminalNames.FUN_DECLARATION_PRIME, 13],
     [NonTerminalNames.VAR_DECLARATION_PRIME, 13]]),
    (13, True, []),
    (14, False, [[';', 18], ['[', 15]]),
    (15, False, [['NUM', 16]]),
    (16, False, [[']', 17]]),
    (17, False, [[';', 18]]),
    (18, True, []),
    (19, False, [['(', 20]]),
    (20, False, [[NonTerminalNames.PARAMS, 21]]),
    (21, False, [[')', 22]]),
    (22, False, [[NonTerminalNames.COMPOUND_STMT, 23]]),
    (23, True, []),
    (24, False, [['int', 25], ['void', 25]]),
    (25, True, []),
    (26, False, [['int', 27], ['void', 30]]),
    (27, False, [['ID', 28]]),
    (28, False, [[NonTerminalNames.PARAM_PRIME, 29]]),
    (29, False, [[NonTerminalNames.PARAM_LIST, 30]]),
    (30, True, []),
    (31, False, [[',', 32], [EPSILON, 34]]),
    (32, False, [[NonTerminalNames.PARAM, 33]]),
    (33, False, [[NonTerminalNames.PARAM_LIST, 34]]),
    (34, True, []),
    (35, False, [[NonTerminalNames.DECLARATION_INITIAL, 36]]),
    (36, False, [[NonTerminalNames.PARAM_PRIME, 37]]),
    (37, True, []),
    (38, False, [['[', 39], [EPSILON, 40]]),
    (39, False, [[']', 40]]),
    (40, True, []),
    (41, False, [['{', 42]]),
    (42, False, [[NonTerminalNames.DECLARATION_LIST, 43]]),
    (43, False, [[NonTerminalNames.STATEMENT_LIST, 44]]),
    (44, False, [['}', 45]]),
    (45, True, []),
    (46, False, [[NonTerminalNames.STATEMENT, 47], [EPSILON, 48]]),
    (47, False, [[NonTerminalNames.STATEMENT_LIST, 48]]),
    (48, True, []),
    (49, False, [[NonTerminalNames.EXPRESSION_STMT, 50], [NonTerminalNames.COMPOUND_STMT, 50], [
     NonTerminalNames.SELECTION_STMT, 50], [NonTerminalNames.ITERATION_STMT, 50], [NonTerminalNames.RETURN_STMT, 50]]),
    (50, True, []),
    (51, False, [[NonTerminalNames.EXPRESSION, 52], ['break', 53], [';', 54]]),
    (52, False, [[';', 54]]),
    (53, False, [[';', 54]]),
    (54, True, []),
    (55, False, [['if', 56]]),
    (56, False, [['(', 57]]),
    (57, False, [[NonTerminalNames.EXPRESSION, 58]]),
    (58, False, [[')', 59]]),
    (59, False, [[NonTerminalNames.STATEMENT, 60]]),
    (60, False, [[NonTerminalNames.ELSE_STMT, 61]]),
    (61, True, []),
    (62, False, [['endif', 63], ['else', 64]]),
    (63, True, []),
    (64, False, [[NonTerminalNames.STATEMENT, 65]]),
    (65, False, [['endif', 63]]),
    (66, False, [['repeat', 67]]),
    (67, False, [[NonTerminalNames.STATEMENT, 68]]),
    (68, False, [['until', 69]]),
    (69, False, [['(', 70]]),
    (70, False, [[NonTerminalNames.EXPRESSION, 71]]),
    (71, False, [[')', 72]]),
    (72, True, []),
    (73, False, [['return', 74]]),
    (74, False, [[NonTerminalNames.RETURN_STMT_PRIME, 75]]),
    (75, True, []),
    (76, False, [[';', 78], [NonTerminalNames.EXPRESSION, 77]]),
    (77, False, [[';', 78]]),
    (78, True, []),
    (79, False, [[NonTerminalNames.SIMPLE_EXPRESSION_ZEGOND, 81], ['ID', 80]]),
    (80, False, [[NonTerminalNames.B, 81]]),
    (81, True, []),
    (82, False, [['=', 83], ['[', 84], [
     NonTerminalNames.SIMPLE_EXPRESSION_PRIME, 87]]),
    (83, False, [[NonTerminalNames.EXPRESSION, 87]]),
    (84, False, [[NonTerminalNames.EXPRESSION, 85]]),
    (85, False, [[']', 86]]),
    (86, False, [[NonTerminalNames.H, 87]]),
    (87, True, []),
    (88, False, [['=', 92], [NonTerminalNames.G, 89]]),
    (89, False, [[NonTerminalNames.D, 90]]),
    (90, False, [[NonTerminalNames.C, 91]]),
    (91, True, []),
    (92, False, [[NonTerminalNames.EXPRESSION, 91]]),
    (93, False, [[NonTerminalNames.ADDITIVE_EXPRESSION_ZEGOND, 94]]),
    (94, False, [[NonTerminalNames.C, 95]]),
    (95, True, []),
    (96, False, [[NonTerminalNames.ADDITIVE_EXPRESSION_PRIME, 97]]),
    (97, False, [[NonTerminalNames.C, 98]]),
    (98, True, []),
    (99, False, [[NonTerminalNames.RELOP, 100], [EPSILON, 101]]),
    (100, False, [[NonTerminalNames.ADDITIVE_EXPRESSION, 101]]),
    (101, True, []),
    (102, False, [['<', 103], ['==', 103]]),
    (103, True, []),
    (104, False, [[NonTerminalNames.TERM, 105]]),
    (105, False, [[NonTerminalNames.D, 106]]),
    (106, True, []),
    (107, False, [[NonTerminalNames.TERM_PRIME, 108]]),
    (108, False, [[NonTerminalNames.D, 109]]),
    (109, True, []),
    (110, False, [[NonTerminalNames.TERM_ZEGOND, 111]]),
    (111, False, [[NonTerminalNames.D, 112]]),
    (112, True, []),
    (113, False, [[NonTerminalNames.ADDOP, 114], [EPSILON, 116]]),
    (114, False, [[NonTerminalNames.TERM, 115]]),
    (115, False, [[NonTerminalNames.D, 116]]),
    (116, True, []),
    (117, False, [['+', 118], ['-', 118]]),
    (118, True, []),
    (119, False, [[NonTerminalNames.FACTOR, 120]]),
    (120, False, [[NonTerminalNames.G, 121]]),
    (121, True, []),
    (122, False, [[NonTerminalNames.FACTOR_PRIME, 123]]),
    (123, False, [[NonTerminalNames.G, 124]]),
    (124, True, []),
    (125, False, [[NonTerminalNames.FACTOR_ZEGOND, 126]]),
    (126, False, [[NonTerminalNames.G, 127]]),
    (127, True, []),
    (128, False, [['*', 129], [EPSILON, 131]]),
    (129, False, [[NonTerminalNames.FACTOR, 130]]),
    (130, False, [[NonTerminalNames.G, 131]]),
    (131, True, []),
    (132, False, [['(', 133], ['ID', 136], ['NUM', 135]]),
    (133, False, [[NonTerminalNames.EXPRESSION, 134]]),
    (134, False, [[')', 135]]),
    (135, True, []),
    (136, False, [[NonTerminalNames.VAR_CALL_PRIME, 135]]),
    (137, False, [['(', 138], [NonTerminalNames.VAR_PRIME, 140]]),
    (138, False, [[NonTerminalNames.ARGS, 139]]),
    (139, False, [[')', 140]]),
    (140, True, []),
    (141, False, [['[', 142], [EPSILON, 144]]),
    (142, False, [[NonTerminalNames.EXPRESSION, 143]]),
    (143, False, [[']', 144]]),
    (144, True, []),
    (145, False, [['(', 146], [EPSILON, 148]]),
    (146, False, [[NonTerminalNames.ARGS, 147]]),
    (147, False, [[')', 148]]),
    (148, True, []),
    (149, False, [['(', 150], ['NUM', 152]]),
    (150, False, [[NonTerminalNames.EXPRESSION, 151]]),
    (151, False, [[')', 152]]),
    (152, True, []),
    (153, False, [[NonTerminalNames.ARG_LIST, 154], [EPSILON, 154]]),
    (154, True, []),
    (155, False, [[NonTerminalNames.EXPRESSION, 156]]),
    (156, False, [[NonTerminalNames.ARG_LIST_PRIME, 157]]),
    (157, True, []),
    (158, False, [[',', 159], [EPSILON, 161]]),
    (159, False, [[NonTerminalNames.EXPRESSION, 160]]),
    (160, False, [[NonTerminalNames.ARG_LIST_PRIME, 161]]),
    (161, True, []),

]

TERMINALS = ['$', EPSILON, 'ID', ';', '[', ']', 'NUM',
             '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return', '=', '==', '<', '+', '-', '*', ]
