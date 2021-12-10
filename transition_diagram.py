from parser_statics import NON_TERMINALS, TERMINALS, ALL_STATES


class NonTerminal:
    __all_non_terminals = []

    def __init__(self, starting_state, first, follow, name):
        self.name = name
        self.starting_state = starting_state
        self.first = first
        self.follow = follow
        NonTerminal.__all_non_terminals.append(self)

    '''staring state of diagram, first, follow'''

    @staticmethod
    def get_nonterminal_by_name(name):
        for nonterminal in NonTerminal.__all_non_terminals:
            if nonterminal.name == name:
                return nonterminal
        print("PROBLEM IN NONTERMINAL GET BY ID DETECTED")
        return None

    @staticmethod
    def correct_relations():
        for nonterminal in NonTerminal.__all_non_terminals:
            nonterminal.set_starting_state()

    def set_starting_state(self):
        self.starting_state = State.get_state_by_id(self.starting_state)

    @staticmethod
    def create_all_non_terminals():
        for name, first, follow, starting_state in NON_TERMINALS:
            NonTerminal(name=name.value, first=first,
                        follow=follow, starting_state=starting_state)


class State:
    __all_states = []

    def __init__(self, id, is_final, children):
        self.is_final = is_final
        self.id = id
        self.children = children
        State.__all_states.append(self)

    '''func is_final
        number
        list[list(edge, next_state,)]
        '''

    @staticmethod
    def get_state_by_id(number):
        for state in State.__all_states:
            if state.id == number:
                return state
        print('PROBLEM IN STATE BY ID DETECTED!')
        return None

    @staticmethod
    def correct_references():
        for state in State.__all_states:
            state.set_non_terminal_edges()

    def set_non_terminal_edges(self):
        for child in self.children:
            if child[0] not in TERMINALS:
                child[0] = NonTerminal.get_nonterminal_by_name(child[0])
            child[1] = State.get_state_by_id(child[1])


    @staticmethod
    def create_all_states():
        for id, is_final, edges in ALL_STATES:
            State(id=id, is_final=is_final, children=edges)
