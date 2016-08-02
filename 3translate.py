import sys, json

from utils import tokenize

from constants import DICT_FILE

sentence = sys.argv[1]

dictionnary = json.load(open(DICT_FILE))

translation = ' '.join([dictionnary.get(word,[['']])[0][0] for word in tokenize(sentence)])

print(translation)