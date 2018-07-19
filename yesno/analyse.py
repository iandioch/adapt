QUESTIONS = ['an', 'ar', 'nach', 'nár']


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
    for w in conll:
        if w.dep == 'top':
            return not w.coarse_pos == 'Verb'


def get_verb_info(morphology):
    # Tense / Aspect / Mood / Autonomous
    INFOS = {
        'PastInd',
        'PresInd',
        'FutInd',
        'Auto'
    }
    morphs = morphology.split('|')
    for t in INFOS:
        if t in morphs:
            yield t


def analyse_verbal_question(conll):
    question_verb = None
    for w in conll:
        print(w.surface, end=' ')
        if w.dep == 'top' and w.coarse_pos == 'Verb':
            question_verb = w
            break
    print()
    if question_verb is None:
        print('No question verb found.')
        for w in conll:
            print(w.surface, '(', w.coarse_pos, '|', w.fine_pos, '-',
                  w.head_obj.surface if w.head_obj is not None else "None", ')', end=' ')
        print()
    else:
        lemma = question_verb.lemma
        tams = [t for t in get_verb_info(question_verb.morphology)]
        print(lemma, tams)
    print('-'*20)


def analyse_copula_question(conll):
    def find_cop(head):
        if head is None:
            return None
        q = [head]
        while len(q):
            w = q.pop(0)
            if w.coarse_pos == 'Cop' or w.surface.lower() in QUESTIONS:
                return w
            for x in w.tails:
                q.append(x)
        return None

    head = None
    for w in conll:
        if w.dep == 'top':
            head = w
            break
    cop = find_cop(head)
    if cop is None:
        print('Could not find question particle.')
        return
    print('Particle =', str(cop))
    predicate = cop.head_obj
    if predicate is None:
        print('Could not find predicate.')
        return
    print('Predicate =', str(predicate))


def analyse(conll_s):
    conll = parse_conll(conll_s)
    if is_copula_question(conll):
        for w in conll:
            print(w.surface, end=' ')
        print()
        print('IS COPULA QUESTION')
        analyse_copula_question(conll)
    else:
        analyse_verbal_question(conll)
