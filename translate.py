import csv, itertools, math
from collections import Counter

nl_dict = {}

def read_trans():
    file = open('generated/fra_nld.csv')
    for row in csv.reader(file, delimiter='\t'):
        row[0] = int(row[0])
        yield row

def group_trans():
    for _, sample in itertools.groupby(read_trans(), key=lambda row: row[0]):
        result = {}
        for lang, rows in itertools.groupby(list(sample), key=lambda row: row[1]):
            result[lang] = list([row[2] for row in rows])
        yield result

# Find some probable translation for a word
"""
Theorie:

A = Trouver les probabilités d'apparition de n'importe quel mot en NEERLANDAIS
B = Faire la meme chose mais seulement pour les phrases dans lesquelles il y a le mot "arbre" dans la version francaise

Maintenant il faut enlever a B la probabilité que le mot soit dans n'importe quel texte via A

TF/IDF

TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)

IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
"""

def tokenize(text):
    text = text.lower()
    for punc in '.;,\'&!/:?"':
        text = text.replace(punc, ' ')
    return [x for x in text.split(' ') if x]


WORD = 'maintenant'
SOURCE = 'fra'
TARGET = 'nld'

print('TRANSLATING:', WORD, 'FROM', SOURCE, 'TO', TARGET)

doc1 = ''
doc2 = ''

for samples in group_trans():
    if len(samples.keys()) == 2:
        source = samples[SOURCE][0]
        target = samples[TARGET][0]
        source_tokens = tokenize(source)
        doc1 += target + ' '
        if WORD in source_tokens:
            doc2 += target + ' '

# it's not really exact, it should only count the word one time per sentence
doc1_tokens = tokenize(doc1)
doc2_tokens = tokenize(doc2)

TF1_counter = Counter(doc1_tokens)
TF2_counter = Counter(doc2_tokens)
TF2 = {word: count/len(doc2_tokens) for word, count in TF2_counter.items()}

# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

TF_IDF = {word: TF2.get(word, 0)*math.log(len(doc1_tokens)/count) for word, count in TF1_counter.items()}

bests = sorted(TF_IDF.items(), key=lambda x: -x[1])[:5]

for word, count in bests:
    print(count, word, TF1_counter[word], TF2_counter[word])

print('RESULT --', bests[0][0], '-- with prob', bests[0][1]*100, '%')