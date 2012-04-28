# Configuration directives goes in here
import logging

LOGGING = {'level': logging.DEBUG,
           'format': '%(asctime)s - %(levelname)8s - %(filename)s:%(lineno)s - %(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S', 
        }

SOURCES = [{'name': 'Argenteam',
            'url': 'http://www.argenteam.net/rss/tvseries_torrents.xml',
            'filters': ['House\.', 'BigBangTheory', 'HowIMetYourMother']
           }
        ]
