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


def create_all_non_terminals():
    for name, first, follow, starting_node in NON_TERMINALS:
        NonTerminal(name=name.value, first=first, follow=follow, starting_node_id=starting_node)
