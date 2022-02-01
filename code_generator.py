from ctypes import Union
from typing import Dict, List
from statics import TokenNames
from pathlib import Path


class CodeGenerator:
    def __init__(self):
        self.AR = []
        self.semantic_stack = []
        self.program_block = Stack(0)
        self.data_block = Stack(100)
        self.temporary_block = Stack(500)
        self.main_starting_addr = 50
        self.symbol_table = None
        self.current_id = None
        self.current_num = None
        self.current_keyword = None
        self.scope_stack = [0]

    def get_temp(self) -> int:
        return self.temporary_block.get_first_empty_cell()

    def find_addr(self, x: str):
        for row in self.symbol_table:
            if row['lexeme'] == x:
                return row['address']

    def sa_assign(self):
        self.add_file()
        self.generate_formatted_code(
            'ASSIGN', self.semantic_stack[-1], self.semantic_stack[-2], '')
        self.semantic_stack.pop()

    def sa_pop(self):
        self.semantic_stack.pop()

    def sa_compute_addr_arr(self):
        t1 = self.get_temp()
        self.generate_formatted_code('MULT', self.semantic_stack[-1], '#4', t1)
        self.semantic_stack.pop()
        t2 = self.get_temp()
        self.generate_formatted_code(
            'ADD', 1, f'#{self.semantic_stack[-1]}', t2)
        self.semantic_stack.pop()
        self.semantic_stack.append(t2)

    def sa_pid(self):
        addr = self.find_addr(self.current_id)
        self.semantic_stack.append(addr)

    def sa_push_num(self):
        self.semantic_stack.append(self.current_num)

    def sa_add_array(self):
        array_len = self.semantic_stack.pop()
        for i in range(int(array_len) - 1):
            empty_cell = self.data_block.get_first_empty_cell()
            self.generate_formatted_code('ASSIGN', '#0', empty_cell, '')
        symbol_row = self.get_symbol_row(self.current_id)
        symbol_row['cell_No'] = array_len

    def sa_add_id(self):
        symbol_row = self.get_symbol_row(self.current_id)
        if symbol_row['type']=='int':
            empty_cell = self.data_block.get_first_empty_cell()
            symbol_row['address'] = empty_cell
            self.generate_formatted_code('ASSIGN', '#0', empty_cell, '')

    def sa_add_id_param(self):
        empty_cell = self.data_block.get_first_empty_cell()
        symbol_row = self.get_symbol_row(self.current_id)
        symbol_row['address'] = empty_cell

    def sa_start_scope(self):
        self.scope_stack.append(len(self.symbol_table))

    def sa_end_scope(self):
        last_scope = self.scope_stack.pop()
        del self.symbol_table[last_scope:]

    def get_symbol_row(self, lexeme):
        for block in self.symbol_table:
            if isinstance(block, dict) and block['lexeme'] == lexeme:
                return block
        return None

    def sa_add_type(self):
        self.symbol_table.append(
            dict(type=self.current_keyword, scope=len(self.scope_stack)))

    def sa_add_int_param(self):
        self.symbol_table.append(
            dict(type='int', scope=len(self.scope_stack)+1))

    def sa_dec_type_func(self):
        self.symbol_table[-1]['declaration type'] = 'func'

    def sa_dec_type_arr(self):
        self.symbol_table[-1]['declaration type'] = 'arr'

    def sa_dec_type_var(self):
        self.symbol_table[-1]['declaration type'] = 'var'

    def sa_dec_type_param(self):
        self.symbol_table[-1]['declaration type'] = 'param'

    def handle_action_symbol(self, token_name: str, token_lexeme: str, action_symbols: List[str]):
        print(token_name, token_lexeme, action_symbols)
        print(self.symbol_table)
        if token_name == TokenNames.ID.value:
            self.current_id = token_lexeme
        elif token_name == TokenNames.NUM.value:
            self.current_num = token_lexeme
        elif token_name == TokenNames.KEYWORD.value:
            self.current_keyword = token_lexeme
        for action_symbol in action_symbols:
            getattr(self, action_symbol)()

    def generate_formatted_code(self, relop: str, s1, s2, s3):
        self.program_block.append(f'({relop}, {(s1)}, {s2}, {s3})')

    def add_file(self):
        o = Path() / 'o.txt'
        o.write_text('\n'.join(self.program_block))


class Stack(list):
    def __init__(self, starting_index: int):
        self.starting_index = starting_index
        self.filled_cells = 0

    def insert(self, __index, __object) -> None:
        return super().insert(int((__index - self.starting_index) / 4), __object)

    def get_first_empty_cell(self) -> int:
        empty_cell = self.starting_index + 4 * self.filled_cells
        self.filled_cells += 1
        return empty_cell


class Record:
    def __init__(self) -> None:
        self.returned_value = None
        self.actual_parameters = {}
