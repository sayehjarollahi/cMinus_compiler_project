from enum import Enum

from transition_diagram import NonTerminal

EPSILON = 'epsilon'


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
    (NonTerminalNames.DECLARATION_INITIAL, ['int', 'void'], ['(', '[', ';', ',', ')'], 9),
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
    (NonTerminalNames.EXPRESSION, ['ID', '(', 'NUM', ], [';', ')', ']', ',', ], 79),
    (NonTerminalNames.B, ['=', '[', '(', '*', '+', '-', '<', '==', EPSILON, ], [';', ')', ']', ',', ], 82),
    (NonTerminalNames.H, ['=', '*', EPSILON, '+', '-', '<', '==', ], [';', ')', ']', ',', ], 88),
    (NonTerminalNames.SIMPLE_EXPRESSION_ZEGOND, ['(', 'NUM', ], [';', ')', ']', ',', ], 93),
    (NonTerminalNames.SIMPLE_EXPRESSION_PRIME, ['(', '*', '+', '-', '<', '==', EPSILON, ], [';', ')', ']', ',', ], 96),
    (NonTerminalNames.C, [EPSILON, '<', '==', ], [';', ')', ']', ',', ], 99),
    (NonTerminalNames.RELOP, ['<', '==', ], ['(', 'ID', 'NUM', ], 102),
    (NonTerminalNames.ADDITIVE_EXPRESSION, ['(', 'ID', 'NUM', ], [';', ')', ']', ',', ], 104),
    (NonTerminalNames.ADDITIVE_EXPRESSION_PRIME, ['(', '*', '+', '-', EPSILON, ], ['<', '==', ';', ')', ']', ',', ],
     107),
    (NonTerminalNames.ADDITIVE_EXPRESSION_ZEGOND, ['(', 'NUM', ], ['<', '==', ';', ')', ']', ',', ], 110),
    (NonTerminalNames.D, [EPSILON, '+', '-', ], ['*', '<', '==', ';', ')', ']', ',', ], 113),
    (NonTerminalNames.ADDOP, ['+', '-', ], ['(', 'ID', 'NUM', ], 117),
    (NonTerminalNames.TERM, ['(', 'ID', 'NUM', ], ['+', '-', ';', ')', '*', '<', '==', ']', ',', ], 119),
    (NonTerminalNames.TERM_PRIME, ['(', '*', EPSILON, ], ['+', '-', '<', '==', ';', ')', ']', ',', ], 122),
    (NonTerminalNames.TERM_ZEGOND, ['(', 'NUM', ], ['+', '-', '<', '==', ';', ')', ']', ',', ], 125),
    (NonTerminalNames.G, ['*', EPSILON, ], ['<', '==', ';', ')', '+', '-', '*', ']', ',', ], 128),
    (NonTerminalNames.FACTOR, ['(', 'ID', 'NUM', ], ['*', '+', '-', ';', ')', '<', '==', ']', ',', ], 132),
    (NonTerminalNames.VAR_CALL_PRIME, ['(', '[', EPSILON, ], ['*', '+', '-', ';', ')', '<', '==', ']', ',', ], 137),
    (NonTerminalNames.VAR_PRIME, ['[', EPSILON, ], ['*', '+', '-', ';', ')', '<', '==', ']', ',', ], 141),
    (NonTerminalNames.FACTOR_PRIME, ['(', EPSILON, ], ['*', '+', '-', '<', '==', ';', ')', ']', ',', ], 145),
    (NonTerminalNames.FACTOR_ZEGOND, ['(', 'NUM', ], ['*', '+', '-', '<', '==', ';', ')', ']', ',', ], 149),
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
    (12, False, [[NonTerminalNames.FUN_DECLARATION_PRIME, 13], [NonTerminalNames.VAR_DECLARATION_PRIME, 13]]),
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
    (24, False, [['int', 25],['void', 25]]),
    (25, True, []),
    (26, False, [['int', 27],['void', 30]]),
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
    (38, False, [['[', 39], [EPSILON,40]]),
    (39, False, [[']', 40]]),
    (40, True, []),
    (41, False, [['{', 42]]),
    (42, False, [[NonTerminalNames.DECLARATION_LIST, 43]]),
    (43, False, [[NonTerminalNames.STATEMENT_LIST, 44]]),
    (44, False, [['}', 45]]),
    (45, True, []),
    (46, False, [[NonTerminalNames.STATEMENT, 47],[EPSILON, 48]]),
    (47, False, [[NonTerminalNames.STATEMENT_LIST, 48]]),
    (48, True, []),
    (49, False, [[NonTerminalNames.EXPRESSION_STMT,50],[NonTerminalNames.COMPOUND_STMT,50],[NonTerminalNames.SELECTION_STMT,50],[NonTerminalNames.ITERATION_STMT,50],[NonTerminalNames.RETURN_STMT,50]]),
    (50, True, []),
    (51, False, [[NonTerminalNames.EXPRESSION, 52],['break', 53],[';', 54]]),
    (52, False, [[';', 54]]),
    (53, False, [[';', 54]]),
    (54, True, []),
    (55, False, []),
    (56, False, []),
    (57, False, []),
    (58, False, []),
    (59, False, []),
    (60, False, []),
    (61, True, []),
    (62, False, []),
    (63, True, []),
    (64, False, []),
    (65, False, []),
    (66, False, []),
    (67, False, []),
    (68, False, []),
    (69, False, []),
    (70, False, []),
    (71, False, []),
    (72, True, []),
    (73, False, []),
    (74, False, []),
    (75, True, []),
    (76, False, []),
    (77, False, []),
    (78, True, []),
    (79, False, []),
    (80, False, []),
    (81, True, []),
    (82, False, []),
    (83, False, []),
    (84, False, []),
    (85, False, []),
    (86, False, []),
    (87, True, []),
    (88, False, []),
    (89, False, []),
    (90, False, []),
    (91, True, []),
    (92, False, []),
    (93, False, []),
    (94, False, []),
    (95, True, []),
    (96, False, []),
    (97, False, []),
    (98, True, []),
    (99, False, []),
    (100, False, []),
    (101, True, []),
    (102, False, []),
    (103, True, []),
    (104, False, []),
    (105, False, []),
    (106, True, []),
    (107, False, []),
    (108, False, []),
    (109, True, []),
    (110, False, []),
    (111, False, []),
    (112, True, []),
    (113, False, []),
    (114, False, []),
    (115, False, []),
    (116, True, []),
    (117, False, []),
    (118, True, []),
    (119, False, []),
    (120, False, []),
    (121, True, []),
    (122, False, []),
    (123, False, []),
    (124, True, []),
    (125, False, []),
    (126, False, []),
    (127, True, []),
    (128, False, []),
    (129, False, []),
    (130, False, []),
    (131, True, []),
    (132, False, []),
    (133, False, []),
    (134, False, []),
    (135, True, []),
    (136, False, []),
    (137, False, []),
    (138, False, []),
    (139, False, []),
    (140, True, []),
    (141, False, []),
    (142, False, []),
    (143, False, []),
    (144, True, []),
    (145, False, []),
    (146, False, []),
    (147, False, []),
    (148, True, []),
    (149, False, []),
    (150, False, []),
    (151, False, []),
    (152, True, []),
    (153, False, []),
    (154, True, []),
    (155, False, []),
    (156, False, []),
    (157, True, []),
    (158, False, []),
    (159, False, []),
    (160, False, []),
    (161, True, []),
    45

]

TERMINALS = ['$', EPSILON, 'ID', ';', '[',']','NUM', '(',')', 'int', 'void', ',', '{','}', 'break', 'if', 'endif', 'else', 'repeat', 'until', 'return', '=','==','<','+','-','*',]


