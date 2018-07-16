class Word:
    def __init__(self, index, surface, lemma, coarse_pos, fine_pos, morphology, head, dep, *other):
        self.index = int(index)
        self.surface = surface
        self.lemma = lemma
        self.coarse_pos = coarse_pos
        self.fine_pos = fine_pos
        self.morphology = morphology
        self.head = head
        self.dep = dep
        self.other = other

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return 'Word("{}", "{}", "{}")'.format(self.surface, self.lemma, self.coarse_pos)

'''
Returns whether or not the question is based on the copula.
Eg.
"An broc é sin?" -> True
"An bhfaca tú é sin?" -> False
'''
def is_copula_question(conll):
    return False

def parse_conll(conll_s):
    e = conll_s.split('\n')
    out = []
    for w in e:
        if len(w) == 0 or w[0] == '#':
            continue
        w_obj = Word(*w.split('\t'))
        out.append(w_obj)
    return out

def analyse(conll_s):
    print(parse_conll(conll_s))
