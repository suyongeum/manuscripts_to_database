from nlp.Line import Line
from nltk import pos_tag, word_tokenize


def tag_line(line: Line):
    tokenized = word_tokenize(line.get_processed_string())
    tags = pos_tag(tokenized)
    if len(tags) != line.get_unshortened_size():
        raise RuntimeError('Tagger returned wrong number of tags.')

    word_shift = 0
    tag_shift = 0
    while word_shift != line.original_size:
        if line.words[word_shift].unshortened_size > 1:
            line.words[word_shift].penn_pos_tag = 'N'
            tag_shift += line.words[word_shift].unshortened_size
            word_shift += 1
        else:
            line.words[word_shift].penn_pos_tag = tags[tag_shift][1]
            tag_shift += 1
            word_shift += 1

    if word_shift != line.original_size:
        raise RuntimeError('Not all tags are set.')

    return line
