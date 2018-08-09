import argparse
import pymysql.cursors
import os
from content_file_reader import read_all_content_files
from definitions import find_definitions
from difficulty import calculate_difficulty
from eumdict_sql import create_schema, check_if_content_exists, create_content, \
    create_word, remove_content, create_line
from nlp.Lemmatiser import Lemmatiser
from nlp.Line import Line
from nlp.string_utils import unshorten_line, process_line
import setting

content_files_path = os.path.join(os.path.dirname(os.getcwd()), 'data_manuscripts')

# Connect to the database
connection = pymysql.connect(host           =   setting.DB_HOST,
                             user           =   setting.DB_USER,
                             password       =   setting.DB_PASS,
                             db             =   setting.DB_NAME,
                             charset        =   setting.DB_CHAR,
                             cursorclass    =   pymysql.cursors.DictCursor)

argparser = argparse.ArgumentParser(description='Seeds manuscript data to database')
argparser.add_argument('-r', '--recreate', dest='recreate', action='store_true',
                       help='If set all content will be recreated')
argparser.add_argument('-c', '--content', dest='content', type=int,
                       default=-1, help='Id of content to be recreated')
args = argparser.parse_args()

try:
    if args.recreate:
        create_schema(connection)
        print('schema recreated')
        connection.commit()

    if args.content != -1:
        print('removing {0}'.format(args.content))
        remove_content(connection, args.content)
        connection.commit()

    lemmatiser = Lemmatiser()

    contents = read_all_content_files(content_files_path)
    print('{0} contents found'.format(len(contents)))

    added = 0
    not_found_difficulties_total = []
    not_found_definitions_total = []

    for content in contents:
        if check_if_content_exists(connection, content['id']):
            print('** Skipping "{0}" - exists'.format(content['id']))
            continue
        print('**  Inserting "{0}" content with {1} lines'.format(content['id'], len(content['lines'])))

        create_content(connection, content)

        for i, text in enumerate(content['lines']):
            line = Line.from_string(text, line_id=i+1, content_id=content['id'])
            if line.original_size == 0:
                print('Empty line found in {0}'. format(content['id']))
                continue
            line = unshorten_line(line)
            line = process_line(line)
            line = lemmatiser.lemmatise_line(line)
            line, not_found_difficulties = calculate_difficulty(connection, line)
            line, not_found_definitions = find_definitions(connection, line)
            not_found_difficulties_total.extend(not_found_difficulties)
            not_found_definitions_total.extend(not_found_definitions)
            create_line(connection,
                        content_id=content['id'],
                        line_order=i + 1,
                        text=line.get_original_string(),
                        difficulty=line.get_difficulty())

            for wi, word in enumerate(line.words):

                create_word(connection,
                            content_id=content['id'],
                            line_order=i + 1,
                            word_order=wi + 1,
                            original=word.original,
                            difficulty=word.difficulty,
                            definition=word.definition,
                            pos=word.definition_pos)

        added += 1

    connection.commit()
    print('-------------------------------------')
    print('Finished!')
    print('Added contents: {0}'.format(added))
    print('Not found definitions: {0}'.format(len(not_found_definitions_total)))
    print('Not found definitions (unique): {0}'.format(len(set(not_found_definitions_total))))
    print('Not found difficulties: {0}'.format(len(not_found_difficulties_total)))
    print('Not found difficulties (unique): {0}'.format(len(set(not_found_difficulties_total))))

except:
    raise

finally:
    connection.close()
