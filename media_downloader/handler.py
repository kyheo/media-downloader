import os
import logging
import urllib2
import sqlite3
import shutil

import smtplib
from email.mime.text import MIMEText

import periscope

from media_downloader import utils

_DB = sqlite3.connect('.database')

def handle(configs, content):
    '''Handle content properly'''
    for config in configs[content['type']]:
        content = config['handler'](config, content)


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
    '''Executes command and send the parameters as configured
    
    Configuration
    * command : Command to run. Content fields should be added as said in here:
                http://docs.python.org/library/stdtypes.html#str.format
                Ex: /path/to/command {link}
    * fields: Fields that should be extracted from content to be used as
              command params.
    '''
    kwargs = utils.format_parameters(content, config['fields'])
    cmd = config['command'].format(**kwargs)
    logging.info('Running %s', cmd)
    os.system(cmd)
    return content


def download_file(config, content):
    '''Downloads a link as specified
    
    Configuration
    * dst_file: Destination file. Content fields should be adeda as said in
                here: http://docs.python.org/library/stdtypes.html#str.format
                Ex: /path/to/new_{link}_destination
    * dst_fields: Fields that should be extracted from content to be used as
                  command params.
    
    '''
    logging.info('Downloading %s', content['name'])
    kwargs = utils.format_parameters(content, config['dst_fields'])
    dst_file = config['dst_file'].format(**kwargs)
    f = urllib2.urlopen(content['link'])
    o = open(dst_file,'wb')
    o.write(f.read())
    o.close()
    f.close()
    return content


def subtitles_periscope(config, content):
    '''Download subtitles using periscope. 
    
    Sections of periscope bin script are replicated in here.
    Content list has the files that require subtitles.

    Configuration:
    * cache_folder: Path to periscope cache folder.
    * langs: List of languages for the subtitles.
    '''
    logging.info('Downloading subtitles with Periscope for %s', content['link'])
    periscope_client = periscope.Periscope(config['cache_folder'])
    sub = periscope_client.downloadSubtitle(content['link'], config['langs'])
    if sub:
        content['subtitle'] = True
        content['subtitle_path'] = sub['subtitlepath']
    else:
        raise Exception('No subtitle found')
    return content


def move_files(config, content):
    '''Moves the paths configured into the destination folder.
    
    Configuration:
    * dst_folder: Destination folder for the file/s
    * fields: Fields of content that have source files that should be moved.
    '''
    logging.info('Moving %s files to %s.', content['name'], config['dst_folder'])
    for source_field in config['fields']:
        if source_field in content:
            shutil.move(content[source_field], config['dst_folder'])
    return content


def send_email(config, content):
    '''Sends an email with the information configured
    
    Configuration:
    * email: Dictionary with email informacion
    * subject: Email subject
    * subject_fields: Fields to use in subject
    * body: Email body
    * body_fields: Fields to use in body
    '''
    logging.info('Sending notification email')
    if 'subtitle' in content and content['subtitle']:
        subject = config['subject']
        if config['subject_fields']:
            kwargs = utils.format_parameters(content, config['subject_fields'])
            subject = subject.format(**kwargs)
        body = config['body']
        if config['body_fields']:
            kwargs = utils.format_parameters(content, config['body_fields'])
            body = body.format(**kwargs)

            msg = MIMEText(body)  
            msg['Subject'] = subject     
            msg['From'] = config['email']['from']
            msg['To'] = ', '.join(config['destination'])
            server = smtplib.SMTP(config['email']['smtp_server'],
                                  config['email']['smtp_port'])
            if config['email']['use_tls']:
                server.starttls()
            server.login(config['email']['smtp_user'], config['email']['smtp_pass'])
            server.sendmail(config['email']['from'], config['destination'],
                            msg.as_string())
            server.quit()
    return content
