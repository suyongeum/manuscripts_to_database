from nltk.corpus import wordnet as wn


class Word:


    def __init__(self, original):
        self.original = original
        self.was_shortened = None
        self.unshortened = None
        self.lemm = []
        self.penn_pos_tag = None
        self.unshortened_size = None
        self.difficulty = 1
        self.processed = None
        self.definition = None
        self.definition_pos = None

    def get_wn_pos_tag(self):
        if self.penn_pos_tag.startswith('J'):
            return wn.ADJ
        elif self.penn_pos_tag.startswith('N'):
            return wn.NOUN
        elif self.penn_pos_tag.startswith('R'):
            return wn.ADV
        elif self.penn_pos_tag.startswith('V'):
            return wn.VERB
        elif self.penn_pos_tag == 'IN':
            return wn.VERB
        elif self.penn_pos_tag == 'PRP':
            return wn.ADJ
        return wn.NOUN

    def __repr__(self):
        return '{0} -> {1}'.format(self.original)
