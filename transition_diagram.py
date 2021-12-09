class NonTerminal:
    __all_non_terminals = []

    def __init__(self, starting_node_id, first, follow, name):
        self.name = name
        self.starting_node = Node.get_node_by_id(starting_node_id)
        self.first = first
        self.follow = follow
        NonTerminal.__all_non_terminals.append(self)

    '''staring node of diagram, first, follow'''

    def get_grammer_by_name(self, name):
        for nonterminal in NonTerminal.__all_non_terminals:
            if nonterminal.name == name:
                return nonterminal
        return None


class Node:
    __all_nodes = []

    def __init__(self, id, is_final, children):
        self.is_final = is_final
        self.id = id
        self.children = children
        Node.__all_nodes.append(self)

    '''func is_final
        number
        list[tuple(edge, next_node)]
        '''

    @staticmethod
    def get_node_by_id(number):
        for node in Node.__all_nodes:
            if node.id == number:
                return node
        return None



