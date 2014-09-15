import pickle

lex_file = '../../data/sentimerge.pk'
data_file = '../../data/morph/preproc_nopos.txt'
simple_file = '../../data/morph/simple_nopos.pk'

with open(lex_file, 'rb') as f:
    lex_pos, lex_pos_weight = pickle.load(f)

pos_dict = dict()

# Record which parts of speech each item has
for key in lex_pos:
    item, pos = key.rsplit('_', maxsplit=1)
    pos_dict.setdefault(item, set()).add(pos)

# Pick the highest weighted part of speech, average if needed
# Perhaps this could be done more cleverly
lex = dict()
weight = dict()
for item, pos_set in pos_dict.items():
    high = 0
    new_set = set()
    for pos in pos_set:
        w = lex_pos_weight[item + '_' + pos]
        if w > high:
            high = w
            new_set = {pos}
        elif w == high:
            new_set.add(pos)
    weight[item] = high
    value = 0
    for pos in new_set:
        value += lex_pos[item + '_' + pos]
    value /= len(new_set)
    lex[item] = value

# Fetch sentiment scores for each compound and lemma
simple = []
with open(data_file, 'r') as f:
    for line in f:
        comp, rest = line.strip().split('\t')
        lemmas = rest.split(',')
        try:
            comp_sent = lex[comp]
            comp_weight = weight[comp]
        except KeyError:
            continue
        lemma_sent = []
        for lem in lemmas:
            try:
                lemma_sent.append(lex[lem])
            except KeyError:
                lemma_sent.append(0)
        simple.append((comp_sent, tuple(lemma_sent), comp_weight))
        print(comp, comp_sent, lemmas, lemma_sent, comp_weight)

# Save data points
with open(simple_file, 'wb') as f:
    pickle.dump(simple, f)