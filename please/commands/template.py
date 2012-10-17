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

from .wordmatch import similarity
import os.path
from collections import defaultdict, Counter

WORD = 0
ARGUMENT = 1
PATH = 2
LIST = 3

CUTOFF = 0.8

class Template:
    def __init__(self, definition, help = ''):
        stokens = self._split(definition)
        self.__build_finite_automata(stokens)
        self.help_text = help

    def _split(self, definition):
        stokens = []
        for s in definition.split():
            i = 0
            l = len(s)
            j = l
            while i < l and s[i] == '[':
                i += 1
            while j > 0 and s[j-1] == ']':
                j -= 1
            if s.find('[', i, j) >= 0:
                j += 1
            left = i
            right = l - j
            has = bool(left and right and i != j)
            m = min(left, right)
            left -= m
            right -= m
            left += has
            right += has
            stokens.extend(s[:left])
            if i < j:
                stokens.append(s[i:j])
            stokens.extend(s[l - right:])
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
            return WORD, [token]

    def __build_finite_automata(self, stokens):
        tokens = []
        fmtokens = []
        eps_stack = []
        epsilons = defaultdict(list)
        pos = 0
        for s in stokens:
            if s == '[':
                eps_stack.append(pos)
                fmtokens.append('[')
            elif s == ']':
                was = eps_stack.pop()
                epsilons[was].append(pos)
                fmtokens.append(']')
            else:
                token = self._parse_token(s)
                tokens.append(token)
                pos += 1

        def _epsilon_chain(pos):
            yield pos
            for next in epsilons[pos]:
                #yield from _epsilon_chain(next)
                for there in _epsilon_chain(next):
                    yield there

        self.epsilons = epsilons

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
        and all possible end states (even if match is not complete),
        as keys in a dictionary whose values are ratios.'''
        l = len(self.tokens)
        links = []
        states = {state: -1 for state in self.starts}
        ratios = {state: 0 for state in self.starts}
        for element in sequence:
            new_states = {}
            new_ratios = {}
            for state in states:
                ratio = ratios[state]
                if state == l:
                    continue # past end there is Nihil
                keys, vals = self.automata[state]
                if keys is not None:
                    delta = similarity(keys, element)
                    if delta < CUTOFF:
                        continue
                    ratio += delta
                for val in vals:
                    if new_ratios.get(val, -1) < ratio:
                        new_states[val] = state
                        new_ratios[val] = ratio
            states = new_states
            ratios = new_ratios
            links.append(states)
        if l not in links[-1]:
            return None, max(ratios.values()) if ratios else 0, ratios
        state = l
        results = {}
        for i in range(len(links) - 1, -1, -1):
            state = links[i][state]
            results.setdefault(state, []).append(sequence[i])
        
        result = {}
        total = 0
        for i, token in enumerate(self.tokens):
            type, arg = token
            if i not in results:
                continue
            if type == ARGUMENT:
                result[arg] = results[i][0]
            elif type == PATH:
                result[arg] = os.path.normpath(results[i][0])
            elif type == LIST:
                results[i].reverse()
                result[arg] = results[i]
        return result, ratios[l], ratios

    def match(self, sequence):
        return self.match_ratio_states(sequence)[0]

    def match_ratio(self, sequence):
        return self.match_ratio_states(sequence)[:2]

    @staticmethod
    def _beautiful(token):
        if isinstance(token, str):
            return token
        elif len(token) == 2 and token[1].startswith(token[0]):
            return '{}[{}]'.format(token[0], token[1][len(token[0]):])
        else:
            return '|'.join(token)

    def format(self):
        from colorama import Style
        if self.help_text.startswith('!suppress'):
            return None
        format = Style.BRIGHT + '{}' + Style.RESET_ALL
        begins = []
        ends = Counter()
        beautiful = self._beautiful
        for begin in range(len(self.tokens)):
            they = self.epsilons[begin]
            begins.append(len(they))
            ends += Counter(they)
        
        ans = []
        for i, token in enumerate(self.tokens):
            type, arg = token
            s = beautiful(arg)
            if type == LIST:
                s += '...'
            if type == WORD:
                s = format.format(s)
            ans.append('[' * begins[i] + s + ']' * ends[i + 1])

        return ' '.join(ans)

    def help(self):
        if not self.help_text.startswith('!suppress'):
            return '{}\n{}'.format(self.format(), self.help_text)
        else:
            return None

    def __str__(self):
        return 'Template({})'.format(self.format())

    __repr__ = __str__
