from eumdict_sql import find_definition
from nlp.string_utils import has_digits, is_abbreviation, is_name


def find_definitions(con, line):
    not_found_words = []

    for i, word in enumerate(line.words):

        if word.was_shortened:
            continue

        found = False
        for form in word.lemm:
            found_definitions = find_definition(con, form.lower())
            if len(found_definitions) > 0:
                found_definitions.sort(key=lambda x: len(x['definition']), reverse=True)
                word.definition = found_definitions[0]['definition']
                word.definition_pos = found_definitions[0]['pos']
                found = True
                break

        if not found:
            print('Not found definition {0}-{1}: {2}'.format(line.content_id, line.line_id, word.lemm))
            not_found_words.append(word)

    return line, not_found_words
