import urllib2
import re
import feedparser
import logging


def create_content(type_, name, link, extra=None):
    '''Create content dictionary'''
    return {'type': type_,
            'name': name,
            'link': link,
            'extra': extra}


def fetch_content(configs):
    '''Fetch content from sources'''
    content = []
    for config in configs:
        logging.info('Fetching from %s', config['name'])
        content += config['handler'](config)
    return content


def argenteam(config):
    ''' Argenteam RSS feed parser
    Returned Types: argenteam-magnet and argenteam-torrent

    Configuration:
    {'name': 'Argenteam',
     'url': 'http://www.argenteam.net/rss/tvseries_torrents.xml',
     'filters': ['House\.', 'BigBangTheory', 'HowIMetYourMother']
    }
    '''
    filtered = []
    raw_content = feedparser.parse(urllib2.urlopen(config['url']).read())
    if not raw_content['entries']:
        logging.info(raw_content['feed'])
    else:
        # @TODO Improve this 3 for's
        filters = []
        for f in config['filters']:
            filters.append(re.compile(f))
        for entry in raw_content['entries']:
            for f in filters:
                if f.match(entry['title']):
                    if entry['link'].startswith('magnet'):
                        type_ = 'argenteam-magnet'
                    else:
                        type_ = 'argenteam-torrent'
                    tmp_content = create_content(type_, entry['title'],
                        entry['link'])
                    filtered.append(tmp_content)
                    break
    return filtered
