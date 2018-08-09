from eumdict_sql import find_word_difficulty
from nlp.string_utils import has_digits, is_abbreviation, is_name


def calculate_difficulty(con, line):
    not_found_words = []

    for i, word in enumerate(line.words):

        if word.was_shortened:
            word.difficulty = 1
            continue
        if has_digits(word.original):
            word.difficulty = 1
            continue
        if is_abbreviation(word.original):
            word.difficulty = 1
            continue
        if i != 0 and is_name(word.original):
            word.difficulty = 1
            continue

        found = False
        for form in word.lemm:
            found_form_words = find_word_difficulty(con, form.lower())
            if len(found_form_words) > 1:
                print('More than one difficulty entry found in the database: {0}'.format(word.original))
                word.difficulty = found_form_words[0]
                found = True
                break
            if len(found_form_words) == 1:
                word.difficulty = found_form_words[0]
                found = True
                break

        if not found:
            print('Not found difficulty {0}-{1}: {2}'.format(line.content_id, line.line_id, word.lemm))
            not_found_words.append(word)

    return line, not_found_words
