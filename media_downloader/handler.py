import os
import logging
import urllib2

def handle(configs, content):
    '''Handle content properly'''
    for config in configs[content.type]:
        logging.info('Handling %s - %s', config['name'], content.name)
        config['handler'](config, content)


def _format_parameters(content, fields):
    '''Format parameters accordingly'''
    kwargs = {}
    for field in fields:
        kwargs[field] = getattr(content, field) 
    return kwargs


def system_command(config, content):
    '''Executes command and send the parameters as configured'''
    kwargs = _format_parameters(content, config['fields'])
    cmd = config['command'].format(**kwargs)
    os.system(cmd)


def download_file(config, content):
    '''Downloads a link as specified'''
    kwargs = _format_parameters(content, config['dst_fields'])
    dst_file = config['dst_file'].format(**kwargs)
    f = urllib2.urlopen(content.link)
    o = open(dst_file,'wb')
    o.write(f.read())
    o.close()
    f.close()
