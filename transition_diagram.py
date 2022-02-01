import json

from parser_statics import NONTERMINALS_FILE_PATH, STATES_FILE_PATH, TERMINALS


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
        with open(NONTERMINALS_FILE_PATH, 'r') as nonterminals_input_file:
            all_nonterminals = json.load(nonterminals_input_file)
            for nonterminal in all_nonterminals:
                NonTerminal(**nonterminal)


class State:
    __all_states = []

    def __init__(self, id, is_final, children):
        self.is_final = is_final
        self.id = id
        self.children = children
        State.__all_states.append(self)

    '''func is_final
        number
        list[list(edge, next_state, action_symbol)]
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
        with open(STATES_FILE_PATH, 'r') as states_input_file:
            all_states = json.load(states_input_file)
            for state in all_states:
                temp = State(**state)
                for child in temp.children:
                    if len(child)==2:
                        child.append(False)
