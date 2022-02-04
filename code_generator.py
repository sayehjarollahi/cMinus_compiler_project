from typing import List
from statics import TokenNames
from pathlib import Path


class CodeGenerator:
    def __init__(self):
        self.ar_stack = []
        self.ar_temp_stack = []
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
        self.current_func = None
        self.main_return_stack = []
        self.while_stack = []

    def define_output_func(self):
        self.symbol_table.append(dict(
            lexeme='output',
            address=0,
            scope=float('inf'),
            type='void',
        ))

    def get_temp(self) -> int:
        return self.temporary_block.get_first_empty_cell()

    def find_addr(self, lexeme: str):
        try:
            row = self.get_symbol_row(lexeme)
        except SymbolNotFound:
            raise SymbolNotFound()
        return row['address']

    def sa_assign(self):
        self.generate_formatted_code(
            'ASSIGN', self.semantic_stack[-1], self.semantic_stack[-2], '')
        first = self.get_type(self.semantic_stack.pop())
        second = self.get_type(self.semantic_stack[-1])
        if first != 'int':
            raise_expression_type_exception('int', first)
        if second != 'int':
            raise_expression_type_exception('int', second)

    def sa_pop(self):
        self.semantic_stack.pop()

    def sa_compute_addr_arr(self):
        t1 = self.get_temp()
        self.generate_formatted_code('MULT', self.semantic_stack[-1], '#4', t1)
        self.semantic_stack.pop()
        t2 = self.get_temp()
        self.generate_formatted_code(
            'ADD', t1, self.semantic_stack[-1], t2)
        self.semantic_stack.pop()
        self.semantic_stack.append(f'@{t2}')

    def sa_pid(self):
        try:
            addr = self.find_addr(self.current_id)
        except SymbolNotFound:
            self.semantic_stack.append(float('inf'))
            raise SemanticErrorException(f'Semantic Error! \'{self.current_id}\' is not defined.')
        self.semantic_stack.append(addr)

    def sa_push_num_dec(self):
        self.semantic_stack.append(self.current_num)

    def sa_push_num(self):
        self.semantic_stack.append(f'#{self.current_num}')

    def sa_add_array(self):
        array_len = self.semantic_stack.pop()
        for _ in range(int(array_len) - 1):
            empty_cell = self.data_block.get_first_empty_cell()
            self.generate_formatted_code('ASSIGN', '#0', empty_cell, '')
        symbol_row = self.get_symbol_row(self.current_id)
        addr = symbol_row['address']
        empty_cell = self.data_block.get_first_empty_cell()
        self.generate_formatted_code('ASSIGN', f'#{addr}', empty_cell, '')
        symbol_row['address'] = empty_cell
        symbol_row['cell_No'] = array_len

    def sa_add_type(self):
        self.symbol_table[-1]['type'] = self.current_keyword
        self.symbol_table[-1]['scope'] = len(self.scope_stack)
        addr = self.symbol_table[-1]['address']
        self.generate_formatted_code('ASSIGN', '#0', addr, '')

    def sa_add_type_param(self):
        self.symbol_table[-1]['type'] = self.current_keyword
        self.symbol_table[-1]['scope'] = len(self.scope_stack) + 1
        addr = self.symbol_table[-1]['address']
        row = self.get_symbol_row(self.current_func)
        row['params_addr'].append(addr)

    def sa_add_id(self):
        empty_cell = self.data_block.get_first_empty_cell()
        self.symbol_table.append(
            dict(lexeme=self.current_id, address=empty_cell))

    def sa_add_int_param(self):
        self.symbol_table.append(
            dict(type='int', scope=len(self.scope_stack) + 1))

    def sa_add_id_param(self):
        self.symbol_table[-1]['lexeme'] = self.current_id
        empty_cell = self.data_block.get_first_empty_cell()
        self.symbol_table[-1]['address'] = empty_cell
        row = self.get_symbol_row(self.current_func)
        row['params_addr'].append(empty_cell)

    def sa_dec_type_param(self):
        self.symbol_table[-1]['declaration type'] = 'param'

    def sa_define_int_param(self):
        self.symbol_table[-1]['param type'] = 'var'

    def sa_define_arr_param(self):
        self.symbol_table[-1]['param type'] = 'arr'

    def sa_start_scope(self):
        self.scope_stack.append(len(self.symbol_table))

    def sa_end_scope(self):
        last_scope = self.scope_stack.pop()
        del self.symbol_table[last_scope:]

    def get_symbol_row(self, lexeme):
        for row in reversed(self.symbol_table):
            if row['lexeme'] == lexeme:
                return row
        raise SymbolNotFound()

    def get_symbol_row_by_address(self, address):
        for row in self.symbol_table:
            if row['address'] and row['address'] == address:
                return row
        return None

    def sa_dec_type_func(self):
        row = self.symbol_table[-1]
        row['declaration type'] = 'func'
        row['params_addr'] = []
        self.current_func = row['lexeme']
        if row['lexeme'] != 'main':
            self.sa_save()
            self.semantic_stack.append(row['address'])
        if row['type'] == 'int':
            row['return'] = self.data_block.get_first_empty_cell()
        else:
            row['return'] = 0

    def sa_dec_type_arr(self):
        if self.symbol_table[-1]['type'] == 'void':
            lexeme = self.symbol_table[-1]['lexeme']
            self.symbol_table.pop()
            raise SemanticErrorException(f'Semantic Error! Illegal type of void for \'{lexeme}\'')
        self.symbol_table[-1]['declaration type'] = 'arr'

    def sa_dec_type_var(self):
        if self.symbol_table[-1]['type'] == 'void':
            lexeme = self.symbol_table[-1]['lexeme']
            self.symbol_table.pop()
            raise SemanticErrorException(f'Semantic Error! Illegal type of void for \'{lexeme}\'')
        self.symbol_table[-1]['declaration type'] = 'var'

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
        self.while_stack.append(True)
        self.semantic_stack.append(len(self.program_block))

    def sa_end_while_scope(self):
        self.while_stack.pop()

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
        if not self.while_stack:
            raise SemanticErrorException('Semantic Error! No \'repeat ... until\' found for \'break\'.')
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
            sign, self.semantic_stack[-2], self.semantic_stack[-1], temp)
        first = self.semantic_stack.pop()
        second = self.semantic_stack.pop()
        self.semantic_stack.append(temp)
        first_type, second_type = self.get_type(first), self.get_type(second)
        if first_type != 'int':
            raise_expression_type_exception('int', first_type)
        if second_type != 'int':
            raise_expression_type_exception('int', second_type)

    def get_type(self, variable):
        if str(variable) == '0':
            return 'void'
        if str(variable).startswith('#'):
            return 'int'
        elif str(variable).startswith('@'):
            return 'int'
        elif self.is_addr_in_temprorary(variable):
            return 'int'
        row = self.get_symbol_row_by_address(variable)
        type = row['declaration type']
        if type == 'param':
            type = row['param type']
        if type == 'arr':
            return 'array'
        elif type == 'func':
            return 'func'
        elif type == 'var':
            return 'int'

    def sa_def_arithmetic(self):
        self.symbol_stack.append(self.current_symbol)

    def sa_add_condition(self):
        symbol = self.symbol_stack.pop()
        sign = 'EQ'
        temp = self.get_temp()
        if symbol == '<':
            sign = 'LT'
        self.generate_formatted_code(
            sign, self.semantic_stack[-2], self.semantic_stack[-1], temp)
        first = self.semantic_stack.pop()
        second = self.semantic_stack.pop()
        self.semantic_stack.append(temp)
        first_type, second_type = self.get_type(first), self.get_type(second)
        if first_type != 'int':
            raise_expression_type_exception('int', first_type)
        if second_type != 'int':
            raise_expression_type_exception('int', second_type)

    def handle_action_symbol(self, token_name: str, token_lexeme: str, action_symbols: List[str]):
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

    def sa_create_ar(self):
        control_link = None if len(self.ar_stack) == 0 else self.ar_stack[-1]
        ar = Record(lexeme=self.current_id, control_link=control_link)
        current_row = self.get_symbol_row(ar.lexeme)
        for record in reversed(self.ar_stack):
            row = self.get_symbol_row(record.lexeme)
            if row['scope'] < current_row['scope']:
                ar.acceyss_link = record
                break
        self.ar_temp_stack.append(ar)

    def sa_call_func(self):
        record = self.ar_temp_stack.pop()
        if record.lexeme == 'output':
            self.handle_output(record)
            return
        row = self.get_symbol_row(record.lexeme)
        self.ar_stack.append(record)
        for param, actual_param in zip(row['params_addr'], record.actual_parameters):
            self.generate_formatted_code('ASSIGN', actual_param, param, '')
        self.generate_formatted_code(
            'ASSIGN', f'#{len(self.program_block) + 2}', self.semantic_stack.pop(),
            '')  # self.semantic_stack[-1] = func['address']
        self.generate_formatted_code('JP', row['start_addr'], '', '')
        if row['type'] == 'int':
            t = self.get_temp()
            self.generate_formatted_code('ASSIGN', row['return'], t, '')
            self.semantic_stack.append(t)
        else:
            self.semantic_stack.append(row['return'])
        self.check_func_call_valid(record, row['params_addr'])

    def handle_output(self, record):
        if len(record.actual_parameters) != 1:
            raise SemanticErrorException('Semantic Error! Mismatch in numbers of arguments of \'output\'.')
        if self.get_type(record.actual_parameters[0]) != 'int':
            raise_parameter_type_exception(1, 'output', 'int', self.get_type(record.actual_parameters[0]))
        addr = record.actual_parameters[0]
        self.generate_formatted_code('PRINT', addr, '', '')

    def sa_assign_param(self):
        param = self.semantic_stack.pop()
        self.ar_temp_stack[-1].actual_parameters.append(param)

    def sa_add_start_addr(self):
        row = self.get_symbol_row(self.current_func)
        row['start_addr'] = len(self.program_block)

    def sa_return(self):
        row = self.get_symbol_row(self.current_func)
        if row['type'] == 'int':
            self.generate_formatted_code(
                'ASSIGN', self.semantic_stack.pop(), row['return'], '')
        if self.current_func != 'main':
            addr = row['address']
            self.generate_formatted_code(
                'JP', f'@{addr}', '', '')
        else:
            self.main_return_stack.append(len(self.program_block))
            self.program_block.append('')

    def sa_last_return(self):
        if self.current_func != 'main':
            self.generate_formatted_code(
                'JP', f'@{self.semantic_stack[-1]}', '', '')
            self.semantic_stack.pop()
            self.sa_jp()
        else:
            for i in reversed(self.main_return_stack):
                self.insert_formatted_code(
                    i, 'JP', len(self.program_block), '', '')

    def check_func_call_valid(self, record, func_params):
        if len(record.actual_parameters) != len(func_params):
            raise SemanticErrorException(f'Semantic Error! Mismatch in numbers of arguments of \'{record.lexeme}\'.')
        index = 0
        for record_param, func_param in zip(record.actual_parameters, func_params):
            index += 1
            record_param_row = self.get_symbol_row_by_address(record_param)
            func_param_type = self.get_symbol_row_by_address(func_param)['param type']
            if str(record_param).startswith('#') or self.is_addr_in_temprorary(record_param) or \
                    record_param_row['declaration type'] == 'var':
                if func_param_type == 'arr':
                    raise_parameter_type_exception(index, record.lexeme, 'array', 'int')
            elif record_param_row['declaration type'] == 'arr' and func_param_type == 'var':
                raise_parameter_type_exception(index, record.lexeme, 'int', 'array')
            elif record_param_row['declaration type'] == 'func':
                func_param_type = 'int' if func_param_type == 'var' else 'array'
                raise_parameter_type_exception(index, record.lexeme, func_param_type, 'func')

    def is_addr_in_temprorary(self, address):
        return address >= self.temporary_block.starting_index

    def is_addr_array(self, address):
        row = self.get_symbol_row_by_address(address)
        if row['type'] == 'addr':
            return True
        return False


class Stack(list):
    def __init__(self, starting_index: int):
        self.starting_index = starting_index
        self.filled_cells = 0

    def get_first_empty_cell(self) -> int:
        empty_cell = self.starting_index + 4 * self.filled_cells
        self.filled_cells += 1
        return empty_cell


class Record:
    def __init__(self, lexeme: str, control_link) -> None:
        self.lexeme = lexeme
        self.actual_parameters = []
        self.control_link = control_link
        self.access_link = None
        self.machine_status = None
        self.local_data = None
        self.temporaries = None


def raise_parameter_type_exception(index, func_name, s1, s2):
    raise SemanticErrorException(
        f'Semantic Error! Mismatch in type of argument {index} '
        f'of \'{func_name}\'. Expected \'{s1}\' but got \'{s2}\' instead.')


def raise_expression_type_exception(expected, got):
    raise SemanticErrorException(f'Semantic Error! Type mismatch in operands, Got {got} instead of {expected}.')


class SemanticErrorException(Exception):
    def __init__(self, message):
        self.message = message


class SymbolNotFound(Exception):
    pass
