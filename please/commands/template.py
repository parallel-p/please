'''Templates for mathing comandline commands.
formal grammar:
    template ::= token *
    token ::= word | wordtail | wordalt | arg | path | list | option
    option ::= '[' template ']'
    word ::= "[a-z]+"
    wordtail ::= word ++ "[" ++ word ++ "]"
    wordalt ::= word ++ ( "|" ++ word ) *
    arg ::= "$" ++ word
    path ::= "/" ++ word
    list ::= word ++ "..."
in EBNF, where `++' means concatenation (no spaces between).'''

from .word_matcher import contains
import os.path

WORD = 0
ARGUMENT = 1
PATH = 2
LIST = 3

class Template:
    def __init__(self, definition):
        stokens = self._split(definition)
        self.__build_finite_automata(stokens)

    def _split(self, definition):
        stokens = []
        for s in definition.split():
            if s[0] == '[':
                stokens.append('[')
                s = s[1:]
                if not s:
                    continue

            if s[-1] == ']' and '[' not in s:
                s = s[:-1]
                if s:
                    stokens.append(s)
                stokens.extend(']')
            else:
                stokens.append(s)
        return stokens


    def _parse_token(self, token):
        if token.startswith('/'):
            return PATH, token[1:]
        elif token.startswith('$'):
            return ARGUMENT, token[1:]
        elif token.endswith('...'):
            token = token[:-3]
            return LIST, token
        elif token.endswith(']'):
            before, after = token[:-1].split('[')
            return WORD, [before, before + after]
        elif '|' in token:
            return WORD, token.split('|')
        else:
            return WORD, token

    def __build_finite_automata(self, stokens):
        tokens = []
        eps_stack = []
        epsilons = {}
        pos = 0
        for s in stokens:
            if s == '[':
                eps_stack.append(pos)
            elif s == ']':
                was = eps_stack.pop()
                epsilons[was] = pos
            else:
                tokens.append(self._parse_token(s))
                pos += 1

        def _epsilon_chain(pos):
            while pos in epsilons:
                yield pos
                pos = epsilons[pos]
            yield pos

        l = len(tokens)
        automata = []
        for i, token in enumerate(tokens):
            type, arg = token
            if type == WORD:
                keys = arg
            else:
                keys = None
            values = [] if type != LIST else [i]
            values.extend(_epsilon_chain(i + 1))
            automata.append((keys, values))

        self.starts = tuple(_epsilon_chain(0))
        self.automata = tuple(automata)
        self.tokens = tuple(tokens)

    def match(self, sequence):
        l = len(self.tokens)
        links = []
        states = {state: -1 for state in self.starts}
        for element in sequence:
            new_states = {}
            for state in states:
                if state == l:
                    continue # past end there is Nihil
                keys, vals = self.automata[state]
                if keys is None or contains(keys, element):
                    for val in vals:
                        new_states[val] = state
            states = new_states
            links.append(states)
        if l not in links[-1]:
            return None
        state = l
        results = {}
        for i in range(len(links) - 1, 0, -1): # yes, everything but first
            state = links[i][state]
            results.setdefault(state, []).append(sequence[i])
        
        result = {}
        for i, token in enumerate(self.tokens):
            type, arg = token
            if type == WORD:
                continue
            if i not in results:
                continue
            elif type == ARGUMENT:
                result[arg] = results[i][0]
            elif type == PATH:
                result[arg] = os.path.normpath(results[i][0])
            elif type == LIST:
                results[i].reverse()
                result[arg] = results[i]
        return result
