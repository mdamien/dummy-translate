
def tokenize(text):
    text = text.lower()
    for punc in '.;,\'&!/:?"»':
        text = text.replace(punc, ' ')
    return [x for x in text.split(' ') if x]