from turtle import pu
from typing import Dict, List, Union
from statics import TokenNames
from pathlib import Path


class CodeGenerator:
    def __init__(self):
        self.AR = []
        self.semantic_stack = []
        self.program_block = []
        self.data_block = Stack(100)
        self.temporary_block = Stack(500)
        self.main_starting_addr = 50
        self.symbol_table = None
        self.current_id = None
        self.current_num = None
        self.current_keyword = None
        self.current_symbol = None
        self.symbol_stack = []
        self.scope_stack = [0]
        self.repeat_stack = []

    def get_temp(self) -> int:
        return self.temporary_block.get_first_empty_cell()

    def find_addr(self, lexeme: str):
        row = self.get_symbol_row(lexeme)
        return row['address']

    def sa_assign(self):
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
            'ADD', t1, f'#{self.semantic_stack[-1]}', t2)
        self.semantic_stack.pop()
        self.semantic_stack.append(t2)

    def sa_pid(self):
        addr = self.find_addr(self.current_id)
        self.semantic_stack.append(addr)

    def sa_push_num_dec(self):
        self.semantic_stack.append(self.current_num)

    def sa_push_num(self):
        self.semantic_stack.append(f'#{self.current_num}')

    def sa_add_array(self):
        array_len = self.semantic_stack.pop()
        for i in range(int(array_len) - 1):
            empty_cell = self.data_block.get_first_empty_cell()
            self.generate_formatted_code('ASSIGN', '#0', empty_cell, '')
        symbol_row = self.get_symbol_row(self.current_id)
        symbol_row['cell_No'] = array_len

    def sa_add_id(self):
        self.symbol_table[-1]['lexeme'] = self.current_id
        symbol_row = self.get_symbol_row(self.current_id)
        if symbol_row['type'] == 'int':
            empty_cell = self.data_block.get_first_empty_cell()
            symbol_row['address'] = empty_cell
            self.generate_formatted_code('ASSIGN', '#0', empty_cell, '')

    def sa_add_id_param(self):
        self.symbol_table[-1]['lexeme'] = self.current_id
        empty_cell = self.data_block.get_first_empty_cell()
        self.symbol_table[-1]['address'] = empty_cell

    def sa_start_scope(self):
        self.scope_stack.append(len(self.symbol_table))

    def sa_end_scope(self):
        last_scope = self.scope_stack.pop()
        del self.symbol_table[last_scope:]

    def get_symbol_row(self, lexeme):
        for row in reversed(self.symbol_table):
            if row['lexeme'] == lexeme:
                return row
        return None

    def sa_add_type(self):
        self.symbol_table.append(
            dict(type=self.current_keyword, scope=len(self.scope_stack)))

    def sa_add_int_param(self):
        self.symbol_table.append(
            dict(type='int', scope=len(self.scope_stack) + 1))

    def sa_dec_type_func(self):
        self.symbol_table[-1]['declaration type'] = 'func'

    def sa_dec_type_arr(self):
        self.symbol_table[-1]['declaration type'] = 'arr'

    def sa_dec_type_var(self):
        self.symbol_table[-1]['declaration type'] = 'var'

    def sa_dec_type_param(self):
        self.symbol_table[-1]['declaration type'] = 'param'

    def sa_save(self):
        self.semantic_stack.append(len(self.program_block))
        self.program_block.append('')

    def sa_jpf(self):
        self.insert_formatted_code(
            self.semantic_stack[-1], 'JPF', self.semantic_stack[-2], len(self.program_block), '')
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def sa_jpf_save(self):
        self.insert_formatted_code(
            self.semantic_stack[-1], 'JPF', self.semantic_stack[-2], len(self.program_block) + 1, '')
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.sa_save()

    def sa_jp(self):
        self.insert_formatted_code(
            self.semantic_stack[-1], 'JP', len(self.program_block), '', '')
        self.semantic_stack.pop()

    def sa_label(self):
        self.semantic_stack.append(len(self.program_block))

    def sa_until(self):
        self.generate_formatted_code(
            'JPF', self.semantic_stack[-1], self.semantic_stack[-2], '')
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def sa_temp_save(self):
        self.sa_save()
        t = self.get_temp()
        self.repeat_stack.append(t)

    def sa_temp(self):
        self.insert_formatted_code(
            self.semantic_stack[-1], 'ASSIGN', f'#{len(self.program_block)}', self.repeat_stack[-1], '')
        self.semantic_stack.pop()
        self.repeat_stack.pop()

    def sa_break(self):
        self.generate_formatted_code(
            'JP', f'@{self.repeat_stack[-1]}', '', '')

    def sa_calc_arithmetic(self):
        sign = 'SUB'
        symbol = self.symbol_stack.pop()
        if symbol == '+':
            sign = 'ADD'
        elif symbol == '*':
            sign = 'MULT'
        temp = self.get_temp()
        self.generate_formatted_code(
            sign, self.semantic_stack[-1], self.semantic_stack[-2], temp)
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.append(temp)

    def sa_def_arithmetic(self):
        self.symbol_stack.append(self.current_symbol)

    def sa_add_condition(self):
        symbol = self.symbol_stack.pop()
        sign = 'EQ'
        temp = self.get_temp()
        if symbol == '<':
            sign = 'LT'
        self.generate_formatted_code(sign, self.semantic_stack[-2], self.semantic_stack[-1], temp)
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.append(temp)


    def handle_action_symbol(self, token_name: str, token_lexeme: str, action_symbols: List[str]):
        print(token_name, token_lexeme, action_symbols)
        print(self.semantic_stack)
        if token_name == TokenNames.ID.value:
            self.current_id = token_lexeme
        elif token_name == TokenNames.NUM.value:
            self.current_num = token_lexeme
        elif token_name == TokenNames.KEYWORD.value:
            self.current_keyword = token_lexeme
        elif token_name == TokenNames.SYMBOL.name:
            self.current_symbol = token_lexeme
        for action_symbol in action_symbols:
            getattr(self, action_symbol)()

    def generate_formatted_code(self, relop: str, s1, s2, s3):
        self.program_block.append(f'({relop}, {s1}, {s2}, {s3})')

    def insert_formatted_code(self, idx: int, relop: str, s1, s2, s3):
        self.program_block[idx] = f'({relop}, {s1}, {s2}, {s3})'

    def add_file(self, x):
        o = Path() / f'{x}.txt'
        o.write_text('\n'.join(
            [f'{index}\t{code}' for index, code in enumerate(self.program_block)]))


class Stack(list):
    def __init__(self, starting_index: int):
        self.starting_index = starting_index
        self.filled_cells = 0

    def get_first_empty_cell(self) -> int:
        empty_cell = self.starting_index + 4 * self.filled_cells
        self.filled_cells += 1
        return empty_cell


class Record:
    def __init__(self) -> None:
        self.returned_value = None
        self.actual_parameters = {}
