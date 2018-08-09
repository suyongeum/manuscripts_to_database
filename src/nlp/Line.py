from nlp.Word import Word


class Line:

    words = []

    def __init__(self, words: list, content_id:int, line_id: int):
        self.words = words
        self.original_size = len(words)
        self.content_id = content_id
        self.line_id = line_id

    def get_unshortened_size(self):
        return sum([w.unshortened_size for w in self.words])

    def get_difficulty(self):
        return sum([w.difficulty for w in self.words]) / self.original_size

    @classmethod
    def from_string(cls, string: str, content_id:int, line_id: int):
        words = string.split()
        return cls([Word(w) for w in words], content_id, line_id)

    def get_original_string(self):
        return ' '.join([w.original for w in self.words])

    def get_unshortened_string(self):
        return ' '.join([w.unshortened if w.was_shortened else w.original for w in self.words])

    def get_processed_string(self):
        return ' '.join([w.processed for w in self.words])

    def get_tagged_string(self):
        return ' '.join([w.original + '[' + w.penn_pos_tag + ']' for w in self.words])

