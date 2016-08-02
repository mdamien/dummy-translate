# build dictionnary

import csv, json, itertools, math
from collections import Counter

from constants import SOURCE, TARGET, TRANS_FILE, DICT_FILE

from utils import tokenize

def read_trans():
    file = open(TRANS_FILE)
    for row in csv.reader(file, delimiter='\t'):
        row[0] = int(row[0])
        yield row


def group_trans():
    for _, sample in itertools.groupby(read_trans(), key=lambda row: row[0]):
        result = {}
        for lang, rows in itertools.groupby(list(sample), key=lambda row: row[1]):
            result[lang] = list([row[2] for row in rows])
        yield result


# I use a whole doc to count words, it's not really exact, it should only count
# the word one time per sentence
doc_source = ''
doc_target = ''

TRANS = list(group_trans())

for samples in TRANS:
    if len(samples.keys()) == 2:
        source = samples[SOURCE][0]
        target = samples[TARGET][0]
        doc_source += source + ' '
        doc_target += target + ' '

source_tokens = tokenize(doc_source)
target_tokens = tokenize(doc_target)

source_tokens_counter = Counter(source_tokens)
target_tokens_counter = Counter(target_tokens)

dico = {}

for word, _ in source_tokens_counter.most_common(1000):
    print('translate', word)

    doc = ''

    for samples in TRANS:
        if len(samples.keys()) == 2:
            source = samples[SOURCE][0]
            target = samples[TARGET][0]
            source_tokens = tokenize(source)
            if word in source_tokens:
                doc += target + ' '

    doc_tokens = tokenize(doc)
    counter = Counter(doc_tokens)
    TF = {word: count/len(doc_tokens) for word, count in counter.items()}
    TF_IDF = {
        word: TF.get(word, 0) * math.log(len(target_tokens) / count)
                    for word, count in target_tokens_counter.items()
    }

    bests = sorted(TF_IDF.items(), key=lambda x: -x[1])[:5]

    """
    for word, count in bests:
        print(count, word, target_tokens_counter[word], counter[word])
    """

    print('\t-->', bests[0][0], '\t(', int(bests[0][1]*100), '% confidence)')
    print()
    dico[word] = bests[:3]
    json.dump(dico, open(DICT_FILE, 'w'), indent=2, sort_keys=True, ensure_ascii=False)