class CodeGenerator:
    def __init__(self, symbol_table):
        self.AR = []
        self.semantic_stack = []
        self.program_block = Stack(0)
        self.data_block = Stack(100)
        self.temporary_block = Stack(500)
        self.main_starting_addr = 50
        self.symbol_table = symbol_table
        self.current_id = None
        self.current_num = None

    def get_temp(self) -> int:
        return self.temporary_block.get_first_empty_cell()

    def find_addr(self, x: str) -> int:
        for row in self.symbol_table:
            if row['lexeme'] == x:
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
            'ADD', 1, f'#{self.semantic_stack[-1]}', t2)
        self.semantic_stack.pop()
        self.semantic_stack.append(t2)

    def sa_pid(self):
        addr = self.find_addr(self.current_id)
        self.semantic_stack.append(addr)

    def sa_push_num(self):
        self.semantic_stack.append(self.current_num)

    def sa_add_array(self):

    def sa_add_id(self):
        empty_cell = self.data_block.get_first_empty_cell()
        for block in self.symbol_table:
            if block['lexeme'] == self.current_id:
                block['address'] = empty_cell
                break
        self.semantic_stack.append(empty_cell)
        self.semantic_stack.append('#0')
        self.sa_assign()

    def handle_action_symbol(self, edge: str, lexeme: str, action_symbol: str):
        if edge == 'ID':
            self.current_id = lexeme
        elif edge == 'NUM':
            self.current_num = lexeme

    def generate_formatted_code(self, relop: str, s1, s2, s3):
        self.program_block.append(f'({relop}, {(s1)}, {s2}, {s3})')


class Stack(list):
    def __init__(self, starting_index: int):
        self.starting_index = starting_index

    def insert(self, __index, __object) -> None:
        return super().insert(int((__index - self.starting_index) / 4), __object)

    def get_first_empty_cell(self) -> int:
        return self.starting_index + 4 * self.__len__


class Record:
    def __init__(self) -> None:
        self.returned_value = None
        self.actual_parameters = {}
