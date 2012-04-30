# Configuration directives goes in here
import logging

from media_downloader import source
from media_downloader import handler

LOGGING = {'level': logging.DEBUG,
           'format': '%(asctime)s - %(levelname)8s - %(filename)s:%(lineno)s - %(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S', 
        }

SOURCES = [{'name': 'Argenteam',
            'handler': source.argenteam,
            'url': 'http://www.argenteam.net/rss/tvseries_torrents.xml',
            'filters': ['House\.', 'BigBangTheory', 'HowIMetYourMother']
           }
        ]

HANDLERS = {
    'argenteam-magnet': [
            {'name': 'BitTorrent - Magnet',
             'handler': handler.system_command,
             'command': '/usr/bin/transmission-remote -a "{link}"',
             'fields': ['link'],
            },
        ],
    'argenteam-torrent': [
            {'name': 'BitTorrent - Torrent',
             'handler': handler.download_file,
             'dst_file': '/Users/kyheo/dev/tmp/{name}.torrent',
             'dst_fields': ['name'],
             },
        ],
    }
