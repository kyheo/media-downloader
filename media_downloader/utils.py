import os

def format_parameters(content, fields):
    '''Format parameters accordingly'''
    kwargs = {}
    for field in fields:
        kwargs[field] = content.get(field, 'undefined')
    return kwargs


def recursive_search(entry):
    files = []
    if os.path.isdir(entry):
        for e in os.listdir(entry):
            files += recursive_search(os.path.join(entry, e))
    elif os.path.isfile(entry):
        files.append(entry)
    return files
