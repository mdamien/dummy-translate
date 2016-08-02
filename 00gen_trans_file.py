import csv


def read_sentences():
    file = open('input/sentences.csv')
    for row in csv.reader(file, delimiter='\t'):
        row[0] = int(row[0])
        yield row


def read_links():
    file = open('input/links.csv')
    for row in csv.reader(file, delimiter='\t'):
        yield (int(col) for col in row)

TARGET_LANGS = ('fra', 'nld')

target = {}  # things we want to keep

for tid, lang, text in read_sentences():
    if lang in TARGET_LANGS:
        target[tid] = [lang, text]

print(len(target), 'targets')

trans = {}

for sid, tid in read_links():
    if tid in target:
        if sid not in trans:
            trans[sid] = set()
        trans[sid].add(tid)

print(len(trans), 'trans')

DEST_FILE = 'generated/fra_nld.csv'
with open(DEST_FILE, 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for sid, tids in trans.items():
        if len(tids) == len(TARGET_LANGS):
            rows = sorted([target[tid] for tid in tids], key=lambda row: row[0])
            langs = set([row[1] for row in rows])
            if len(langs) == len(TARGET_LANGS):
                for row in rows:
                    writer.writerow([str(x) for x in [sid] + row])
print(DEST_FILE, 'done')