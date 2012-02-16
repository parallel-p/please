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

from .wordmatch import contains, similarity, CUTOFF
import os.path

WORD = 0
ARGUMENT = 1
PATH = 2
LIST = 3

def _beautiful(token):
    if isinstance(token, str):
        return token
    elif len(token) == 2 and token[1].startswith(token[0]):
        return '{}[{}]'.format(token[0], token[1][len(token[0]):])
    else:
        return '|'.join(token)

class Template:
    def __init__(self, definition, help = ''):
        stokens = self._split(definition)
        self.__build_finite_automata(stokens)
        self.help = '{}\n{}'.format(self.string, help)

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
            return WORD, (token,)

    def __build_finite_automata(self, stokens):
        tokens = []
        fmtokens = []
        eps_stack = []
        epsilons = {}
        pos = 0
        for s in stokens:
            if s == '[':
                eps_stack.append(pos)
                fmtokens.append('[')
            elif s == ']':
                was = eps_stack.pop()
                epsilons[was] = pos
                fmtokens.append(']')
            else:
                token = self._parse_token(s)
                tokens.append(token)
                fmtokens.append(_beautiful(token[1]))
                pos += 1

        self.string = ' '.join(fmtokens).replace('[ ', '[').replace(' ]', ']')

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

    def match_ratio_states(self, sequence):
        '''Matches sequence against itself.
        Returns a dictionary if match is successful else None,
        a `ratio' depicting how trustful match is,
        and all possible end states (even if match is not complete).'''
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
        states = list(states) # keys only
        if l not in links[-1]:
            return None, 0, states
        state = l
        results = {}
        for i in range(len(links) - 1, -1, -1):
            state = links[i][state]
            results.setdefault(state, []).append(sequence[i])
        
        result = {}
        howmuch = 0
        ratio = 1
        for i, token in enumerate(self.tokens):
            type, arg = token
            if i not in results:
                continue
            if type == WORD:
                ratio = min(ratio,
                            similarity(self.tokens[i][1],
                                    results[i][0]))
                howmuch += 1
            elif type == ARGUMENT:
                result[arg] = results[i][0]
            elif type == PATH:
                result[arg] = os.path.normpath(results[i][0])
            elif type == LIST:
                results[i].reverse()
                result[arg] = results[i]
        return result, (ratio - CUTOFF) * howmuch, states

    def match(self, sequence):

        return self.match_ratio_states(sequence)[0]

    def match_ratio(self, sequence):

        return self.match_ratio_states(sequence)[:2]

    def __str__(self):
        return 'Template({})'.format(self.string)

    __repr__ = __str__
