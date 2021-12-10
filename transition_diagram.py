from parser_statics import NON_TERMINALS, TERMINALS, ALL_NODES


class NonTerminal:
    __all_non_terminals = []

    def __init__(self, starting_node, first, follow, name):
        self.name = name
        self.starting_node = starting_node
        self.first = first
        self.follow = follow
        NonTerminal.__all_non_terminals.append(self)

    '''staring node of diagram, first, follow'''

    @staticmethod
    def get_nonterminal_by_name(name):
        for nonterminal in NonTerminal.__all_non_terminals:
            if nonterminal.name == name:
                return nonterminal
        print("PROBLEM IN NONTERMINAL GET BY ID DETECTED")
        return None

    def correct_relations(self):
        self.starting_node = Node.get_node_by_id(self.starting_node)

    @staticmethod
    def create_all_non_terminals():
        for name, first, follow, starting_node in NON_TERMINALS:
            NonTerminal(name=name.value, first=first,
                        follow=follow, starting_node=starting_node)


class Node:
    __all_nodes = []

    def __init__(self, id, is_final, children):
        self.is_final = is_final
        self.id = id
        self.children = children
        Node.__all_nodes.append(self)

    '''func is_final
        number
        list[list(edge, next_node, is_edge_nonterminal)]
        '''

    @staticmethod
    def get_node_by_id(number):
        for node in Node.__all_nodes:
            if node.id == number:
                return node
        print('PROBLEM IN NODE BY ID DETECTED!')
        return None

    @staticmethod
    def correct_references():
        for node in Node.__all_nodes:
            node.set_non_terminal_edges()

    def set_non_terminal_edges(self):
        for child in self.children:
            if child[0] not in TERMINALS:
                child[0] = NonTerminal.get_nonterminal_by_name(child[0])
                child[1] = Node.get_node_by_id(child[1])

            child[2] = child[0] not in TERMINALS

    @staticmethod
    def create_all_nodes():
        for id, is_final, edges in ALL_NODES:
            Node(id=id, is_final=is_final, children=edges)
