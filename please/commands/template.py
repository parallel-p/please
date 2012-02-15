from .word_matcher import contains
import os.path

WORD = 0
ARGUMENT = 1
PATH = 2
LIST = 3

class Template:
    def __init__(self, definition):
        tokens = definition.split()
        tokens = [self._parse_token(s) for s in tokens]
        self.__build_finite_automata(tokens)

    def _parse_token(self, token):
        absent = False
        if token.endswith('?'):
            absent = True
            token = token[:-1]
        if token.startswith('/'):
            return PATH, token[1:], absent
        elif token.startswith('$'):
            return ARGUMENT, token[1:], absent
        elif token.endswith('...'):
            token = token[:-3]
            return LIST, token, absent
        elif token.endswith(']'):
            before, after = token[:-1].split('[')
            return WORD, [before, before + after], absent
        elif '|' in token:
            return WORD, token.split('|'), absent
        else:
            return WORD, token, absent

    def __build_finite_automata(self, tokens):
        epsilons = []
        l = len(tokens)
        epsilons = [token[2] for token in tokens]
        automata = []
        for i, token in enumerate(tokens):
            type, arg, eps = token
            if type == WORD:
                keys = arg
            else:
                keys = None
            values = [i + 1] if type != LIST else [i, i + 1]
            if i + 1 < l:
                for j in range(i + 1, l):
                    if not epsilons[j]:
                        break
                values.extend(range(i + 2, j + 1))
            automata.append((keys, values))
        for i in range(l):
            if not epsilons[i]:
                break

        self.starts = list(range(i + 1))
        self.automata = automata
        self.tokens = tokens

    def match(self, sequence, basepath):
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
            return {}
        state = l
        results = {}
        for i in range(len(links) - 1, 0, -1): # yes, everything but first
            state = links[i][state]
            results.setdefault(state, []).append(sequence[i])
        
        result = {}
        for i, token in enumerate(self.tokens):
            type, arg, _ = token
            if type == WORD:
                continue
            if i not in results:
                continue
            elif type == ARGUMENT:
                result[arg] = results[i][0]
            elif type == PATH:
                result[arg] = os.path.normpath(os.path.join(basepath,
                                                            results[i][0]))
            elif type == LIST:
                results[i].reverse()
                result[arg] = results[i]
        return result
