import csv, itertools, collections

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
    for punc in '.;,\'&!/:"':
        text = text.replace(punc, ' ')
    return [x for x in text.split(' ') if x]


WORD = 'église'
SOURCE = 'fra'
TARGET = 'nld'

print('TRANSLATING:', WORD, 'FROM', SOURCE, 'TO', TARGET)

all_occ = collections.Counter()
occ = collections.Counter()

for samples in group_trans():
    if len(samples.keys()) == 2:
        source = samples[SOURCE][0]
        target = samples[TARGET][0]
        source_tokens = tokenize(source)
        target_tokens = tokenize(target)
        for token in target_tokens:
            all_occ[token] += 1
        if WORD in source_tokens:
            for token in target_tokens:
                occ[token] += 1

## TF/IDF

# TF(t) = frequency of a word in any sentence
all_occ_sum = sum(all_occ.values())
TF = {word: count/all_occ_sum for word, count in all_occ.items()}


for word, freq in sorted(TF.items(), key=lambda x: -x[1])[:10]:
    print(word, freq)

print()
print('----')
print()

# TF2(t) = frequency of a word in sentences where word occur in french too
occ_sum = sum(occ.values())
TF2 = {word: count/occ_sum for word, count in occ.items()}



for word, freq in occ.most_common(10):
    print(word, freq)

print('###')


for word, freq in sorted(TF2.items(), key=lambda x: -x[1])[:10]:
    print(word, freq)


print()
print('----')
print()

# TF3(t) = TF2/TF
occ_sum = sum(occ.values())
TF3 = [(word, TF2[word]/TF[word]) for word in TF2]

for word, freq in sorted(TF3, key=lambda x: -x[1])[:10]:
    print(word, freq)
