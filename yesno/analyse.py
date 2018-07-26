import json

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
    ans = {
        'type': 'verb',
        'error': None 
    }
    question_verb = None
    for w in conll:
        if w.dep == 'top' and w.coarse_pos == 'Verb':
            question_verb = w
            break
    if question_verb is None:
        ans['error'] = 'No question verb found.'
        return ans
    else:
        lemma = question_verb.lemma
        tams = [t for t in get_verb_info(question_verb.morphology)]
        ans['verb'] = {
            'lemma': question_verb.lemma,
            'surface': question_verb.surface,
            'tams': tams
        }
    return ans

def analyse_copula_question(conll):
    ans = {
        'type': 'copula',
        'error': None
    }
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
        ans['error'] = 'Could not find copula form.'
        return ans
    predicate = cop.head_obj
    if predicate is None:
        ans['error'] = 'Could not find predicate.'
        return ans

    ans['copula'] = {
        'surface': cop.surface,
        'lemma': cop.lemma
    }
    ans['predicate'] = {
        'surface': predicate.surface,
        'lemma': predicate.lemma
    }
    return ans

def analyse(conll_s):
    conll = parse_conll(conll_s)
    ans = {}
    if is_copula_question(conll):
        ans = analyse_copula_question(conll)
    else:
        ans = analyse_verbal_question(conll)
    ans['question'] = ' '.join(w.surface for w in conll)
    print(json.dumps(ans, indent=4, ensure_ascii=False))
