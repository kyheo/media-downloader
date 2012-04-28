import urllib2
import re
import feedparser
import logging
from media_downloader import content_type

class InvalidSourceError(Exception):
    pass

class SourceConfigurationError(Exception):
    pass

class Manager(object):
    '''Manages sources configuration and launches content fetching'''

    def __init__(self, config):
        self.config = config
        self.sources = {'Argenteam': Argenteam}

    def fetch_content(self):
        content = []
        for config in self.config:
            if config['name'] not in self.sources:
                raise InvalidSourceError('Invalid %s source.' % (config['name'],))
            source = self.sources[config['name']](config)
            content += source.fetch_content() 
        return content


# Source classes
class Base(object):
    
    SourceConfigurationError = SourceConfigurationError

    def __init__(self, config):
        self.config = config
        self.check_configuration()

    def check_configuration(self):
        raise NotImplementedError('Must override.')

    def fetch_content(self):
        raise NotImplementedError('Must override.')


class Argenteam(Base):
    ''' Argenteam RSS feed parser

    Configuration:
    {'name': 'Argenteam',
     'url': 'http://www.argenteam.net/rss/tvseries_torrents.xml',
     'filters': ['House\.', 'BigBangTheory', 'HowIMetYourMother']
    }
    '''

    def check_configuration(self):
        if 'url' not in self.config:
            raise self.SourceConfigurationError('Missing rss url in configuration.')
        if 'filters' not in self.config:
            raise self.SourceConfigurationError('Missing filters list in configuration.')

    def fetch_content(self):
        filtered = []
        raw_content = feedparser.parse(urllib2.urlopen(self.config['url']).read())
        if not raw_content['entries']:
            logging.info(raw_content['feed'])
        else:
            # @TODO Improve this 3 for's
            filters = []
            for f in self.config['filters']:
                filters.append(re.compile(f))
            for entry in raw_content['entries']:
                for f in filters:
                    if f.match(entry['title']):
                        filtered.append(self._create_content_type(entry))
                        break
            logging.debug(filtered)
        return filtered

    def _create_content_type(self, entry):
        if entry['link'].startswith('magnet'):
            type_ = content_type.TYPE['magnet']
        else:
            type_ = content_type.TYPE['torrent']
        return content_type.ContentType(type_, entry['title'], entry['link'])
