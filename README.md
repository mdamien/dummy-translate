Small exploration on machine translation

- `sh 0download_input.sh` to download the dataset
- `python3 1gen_trans_file.py` to generated the intermediate translation file
- `python3 2build_dict.py` to generate the translation dictionnary
- 'python3 3translate "your sentence"' to get the translation
You can configure the source and target language for translation in `constants.py`

At the end, you will have a dictionnary from SOURCE to TARGET.

### method = TF/IDF

Intuition is: The translation of a word in gonna appear more in the translated sentences
which contains the word. But we need to take into account the common words (the, I, am,..)
are gonna appear often too.

So, I find the translation for a word by a TF/IDF on the target language sentences where
the word appear in the source language translation too VERSUS all the sentences.

### sample

```shell
> python3 3translate.py "Je suis un petit poisson"
ik ben een klein vis
> python3 3translate.py "La robe est rouge"
de jurk is rood
> python3 3translate.py "Qui a pris mes lunettes ?"
wie heeft ik mijn bril
```