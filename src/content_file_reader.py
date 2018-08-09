from os import listdir
from os.path import isfile, join


def read_all_content_files(dir):
    dir_list = listdir(dir)
    contents = []
    for name in dir_list:
        path = join(dir, name)
        if not isfile(path):
            continue
        split_name = name.split('_')
        content_id = int(split_name[0])
        lines = read_content_file(path)
        contents.append({
            'id': content_id,
            'name': name,
            'lines': lines
        })
    return contents


def read_content_file(path):
    lines = []
    encodings = ['utf-16', 'utf-8', 'ascii']
    for e in encodings:
        try:
            with open(path, encoding=e) as f:
                lines = f.readlines()
                lines = [l.strip(' \t\n\r.') for l in lines]
        except UnicodeError:
            #print('Error in reading ' + path)
            #print('got unicode error with %s , trying different encoding' % e)
            continue
        else:
            #print('opening the file with encoding:  %s ' % e)
            break
    return lines

