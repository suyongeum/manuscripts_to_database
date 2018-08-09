from nlp.Line import Line


contractions = {
    'isn\'t': ['is', 'not'],
    'aren\'t': ['are', 'not'],
    'wasn\'t': ['was', 'not'],
    'weren\'t': ['were', 'not'],
    'don\'t': ['do', 'not'],
    'doesn\'t': ['does', 'not'],
    'didn\'t': ['did', 'not'],
    'can\'t': ['can', 'not'],
    'cannot': ['can', 'not'],
    'we\'re': ['we', 'are'],
    'i\'m': ['I', 'am'],
    'i\'d': ['I', 'would'],
    'it\'s': ['it', 'is'],
    'haven\'t': ['have', 'not'],
    'hasn\'t': ['has', 'not'],
    'hadn\'t': ['had', 'not'],
    'couldn\'t': ['could', 'not'],
    'mightn\'t': ['might', 'not'],
    'mustn\'t': ['must', 'not'],
    'shan\'t': ['shall', 'not'],
    'mayn\'t': ['may', 'not'],
    'shouldn\'t': ['should', 'not'],
    'won\'t': ['will', 'not'],
    'wouldn\'t': ['would', 'not'],
    'daren\'t': ['dare', 'not'],
    'needn\'t': ['need', 'not'],
    'usedn\'t': ['use', 'not'],
    'ain\'t': ['are', 'not'],
    'let\'s': ['let', 'us'],
    'you\'ve': ['you', 'have'],
    'should\'ve': ['should', 'have'],
    'i\'ve': ['I', 'have'],
    'they\'ve': ['they', 'have'],
    'wanna': ['want', 'to'],
    'gonna': ['going', 'to'],
    'gotta': ['got', 'to'],
    'outta': ['out', 'of'],
    'sorta': ['sort', 'of'],
    'that\'s': ['that', 'is'],
    'you\'ll': ['you', 'will'],
    'i\'ll': ['I', 'will'],
    'we\'ll': ['we', 'will'],
    'he\'ll': ['he', 'will'],
    'she\'ll': ['she', 'will'],
    'they\'ll': ['they', 'will'],
    'you\'re': ['you', 'are'],
    'you\'d': ['you', 'would'],
    'he\'d': ['he', 'would'],
    'she\'d': ['she', 'would'],
    'they\'re': ['they', 'are'],
    'we\'ve': ['we', 'have'],
    'could\'ve': ['could', 'have'],
    'who\'ve': ['who', 'have'],
}


def has_digits(word):
    return any(char.isdigit() for char in word)


def is_abbreviation(word):
    return all(char.isupper() for char in word)


def is_name(word):
    return word[0].isupper()


def process_line(line: Line):
    for word in line.words:
        if not word.was_shortened:
            word.processed = word.original.translate({ord(c): None for c in '%&#()@$\'*.,-_`'})
        else:
            word.processed = word.unshortened
    return line


def unshorten_line(line: Line):
    for word in line.words:
        full = contractions.get(word.original.lower(), '')
        if full == '':
            word.unshortened_size = 1
            word.was_shortened = False
        else:
            word.was_shortened = True
            word.unshortened = ' '.join(full)
            word.unshortened_size = len(full)
    return line
