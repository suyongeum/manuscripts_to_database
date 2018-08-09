from nltk.stem import WordNetLemmatizer

from nltk.corpus import wordnet as wn

from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer

from nlp.Line import Line
from nlp.string_utils import unshorten_line
from nlp.tagging import tag_line


class Lemmatiser:

    not_important_words = ['\'', '\'s', '$', '%', '&', '.']

    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.lancaster_stemmer = LancasterStemmer()
        self.porter_stemmer = PorterStemmer()
        self.snowball_stemmer = SnowballStemmer('english')

        wn.ensure_loaded()

    def contractions_filter(self, sentence: str):
        words = sentence.split()
        filtered_words = []
        for word in words:
            if word.lower() in self.contractions:
                filtered_words.extend(self.contractions[word.lower()])
                continue
            filtered_words.append(word)

        return ' '.join(filtered_words)

    def lemmatise_line(self, line: Line):
        line = tag_line(line)
        for word in line.words:
            word.lemm.append(word.original)

            if word.processed not in word.lemm:
                word.lemm.append(word.processed)

            precessed_lemm = self.wnl.lemmatize(word.processed, pos=word.get_wn_pos_tag())
            if precessed_lemm not in word.lemm:
                word.lemm.append(precessed_lemm)

            for tag in [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]:
                lemm = self.wnl.lemmatize(word.processed, pos=tag)
                if lemm not in word.lemm:
                    word.lemm.append(lemm)

            lancaster_stem = self.lancaster_stemmer.stem(word.processed)
            if precessed_lemm not in word.lemm:
                word.lemm.append(lancaster_stem)

            porter_stem = self.porter_stemmer.stem(word.processed)
            if precessed_lemm not in word.lemm:
                word.lemm.append(porter_stem)

            snowball_stem = self.snowball_stemmer.stem(word.processed)
            if precessed_lemm not in word.lemm:
                word.lemm.append(snowball_stem)

        return line

