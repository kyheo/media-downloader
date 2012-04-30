# Configuration directives goes in here
import logging

from media_downloader import source
from media_downloader import handler
from media_downloader import content_type

LOGGING = {'level': logging.DEBUG,
           'format': '%(asctime)s - %(levelname)8s - %(filename)s:%(lineno)s - %(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S', 
        }

SOURCES = [{'name': source.Argenteam.__name__,
            'class': source.Argenteam,
            'url': 'http://www.argenteam.net/rss/tvseries_torrents.xml',
            'filters': ['House\.', 'BigBangTheory', 'HowIMetYourMother']
           }
        ]

HANDLERS = {
    content_type.TYPE['magnet']: [
            {'name': 'BitTorrent - Magnet',
             'handler': handler.system_command,
             'command': '/usr/bin/transmission-remote -a "{link}"',
             'fields': ['link'],
            },
        ],
    content_type.TYPE['torrent']: [
            {'name': 'BitTorrent - Torrent',
             'handler': handler.download_file,
             'dst_file': '/Users/kyheo/dev/tmp/{name}.torrent',
             'dst_fields': ['name'],
             },
        ],
    }
