class CodeGenerator:
    def __init__(self, ):
        self.AR = []
        self.semantic_stack = []
        self.program_block = Stack(0)
        self.data_block = Stack(100)
        self.temporary_block = Stack(500)
        self.main_starting_addr = 50

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

    def get_temp(self) -> int:
        return self.temporary_block.get_first_empty_cell()

    def find_addr(self, x: str) -> int:
        pass

    def generate_formatted_code(self, relop: str, s1: str, s2: str, s3: str) -> str:
        return self.program_block.append(f'({relop}, {s1}, {s2}, {s3})')


class Stack(list):
    def __init__(self, starting_index: int):
        self.starting_index = starting_index

    def insert(self, __index, __object) -> None:
        return super().insert((__index-self.starting_index)/4, __object)

    def get_first_empty_cell(self) -> int:
        return self.starting_index + 4 * self.__len__


class Record:
    def __init__(self) -> None:
        self.returned_value = None
        self.actual_parameters = {}
