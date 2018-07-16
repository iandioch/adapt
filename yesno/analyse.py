class Word:
    def __init__(self, index, surface, lemma, coarse_pos, fine_pos, morphology, head, dep, *other):
        self.index = int(index)
        self.surface = surface
        self.lemma = lemma
        self.coarse_pos = coarse_pos
        self.fine_pos = fine_pos
        self.morphology = morphology
        self.head = int(head)
        self.dep = dep
        self.other = other

        self.head_obj = None
        self.tails = []

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return 'Word("{}", "{}", "{}")'.format(self.surface, self.lemma, self.coarse_pos)


def parse_conll(conll_s):
    e = conll_s.split('\n')
    out = []
    for w in e:
        if len(w) == 0 or w[0] == '#':
            continue
        w_obj = Word(*w.split('\t'))
        out.append(w_obj)

    # Link each word to its tails, and each tail to its head
    for wo in out:
        head = wo.head
        if head == 0:
            # root
            pass
        else:
            out[head-1].tails.append(wo)
            wo.head_obj = out[head-1]
    return out


'''
Returns whether or not the question is based on the copula.
Eg.
"An broc é sin?" -> True
"An bhfaca tú é sin?" -> False
'''


def is_copula_question(conll):
    # TODO
    return False


def analyse_verbal_question(conll):
    for w in conll:
        print(str(w))
    pass


def analyse(conll_s):
    conll = parse_conll(conll_s)
    if is_copula_question(conll):
        # TODO
        pass
    else:
        analyse_verbal_question(conll)
