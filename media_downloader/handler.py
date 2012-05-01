import os
import logging
import urllib2
import sqlite3

_DB = sqlite3.connect('.database')

def handle(configs, content):
    '''Handle content properly'''
    for config in configs[content['type']]:
        content = config['handler'](config, content)


def _format_parameters(content, fields):
    '''Format parameters accordingly'''
    kwargs = {}
    for field in fields:
        kwargs[field] = content.get(field, 'undefined')
    return kwargs


def avoid_duplicated(config, content):
    '''Checks if a link was alredy downloaded'''
    logging.info('Checking duplicated for %s', content['name'])
    c = _DB.cursor()
    c.execute('SELECT count(*) as total FROM files WHERE link = :link',
        {'link': content['link']})
    res = c.fetchone()
    if res[0] > 0:
        raise Exception('Duplicated content file.')
    return content 


def store_link(config, content):
    '''Stores link for future checks'''
    logging.info('Storing link for %s', content['name'])
    c = _DB.cursor()
    c.execute('INSERT INTO files (link) VALUES (:link)',
        {'link': content['link']})
    _DB.commit()
    return content 


def system_command(config, content):
    '''Executes command and send the parameters as configured'''
    kwargs = _format_parameters(content, config['fields'])
    cmd = config['command'].format(**kwargs)
    logging.info('Running %s', cmd)
    os.system(cmd)
    return content


def download_file(config, content):
    '''Downloads a link as specified'''
    logging.info('Downloading %s', content['name'])
    kwargs = _format_parameters(content, config['dst_fields'])
    dst_file = config['dst_file'].format(**kwargs)
    f = urllib2.urlopen(content['link'])
    o = open(dst_file,'wb')
    o.write(f.read())
    o.close()
    f.close()
    return content
