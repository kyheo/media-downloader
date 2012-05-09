# Configuration directives goes in here
import logging

from media_downloader import source
from media_downloader import handler

LOGGING = {'level': logging.DEBUG,
           'format': '%(asctime)s - %(levelname)8s - %(filename)s:%(lineno)s - %(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S', 
           #'filename': '/path/to/filename',
           #'filemode': 'a',
        }

SOURCES = [{'name': 'Argenteam',
            'handler': source.argenteam,
            'url': 'http://www.argenteam.net/rss/tvseries_torrents.xml',
            'filters': ['House\.', 'BigBangTheory', 'HowIMetYourMother']
           },
           {'name': 'Video Files',
            'handler': source.video_files,
            'directory': '/Users/kyheo/dev/tmp/',
            'type': 'periscope-video'
           }
        ]

# Common handlers
avoid_duplicated = {'name': 'Avoid Duplicated downloads',
                    'handler': handler.avoid_duplicated}

store_link = {'name': 'Store link',
              'handler': handler.store_link}

email_config = {'from': 'user@gmail.com', 
                'smtp_server': 'smtp.gmail.com',
                'smtp_user': 'user@gmail.com',
                'smtp_port': 587,
                'smtp_pass': 'password',
                'use_tls': True
               }

argenteam_email = {'name': 'Argenteam - Notify',
             'handler': handler.send_email,
             'email': email_config,
             'destination': ['email'],
             'subject': 'New Movie / Serie download',
             'subject_fields': [],
             'body': '{name} got downloaded.',
             'body_fields': ['name']
             }

# MAIN HANDLERS CONFIG
HANDLERS = {
    'argenteam-magnet': [
            avoid_duplicated,
            {'name': 'BitTorrent - Magnet',
             'handler': handler.system_command,
             'command': '/usr/bin/transmission-remote -a "{link}"',
             'fields': ['link'],
            },
            store_link,
            argenteam_email,
        ],
    'argenteam-torrent': [
            avoid_duplicated,
            {'name': 'BitTorrent - Torrent',
             'handler': handler.download_file,
             'dst_file': '/Users/kyheo/dev/tmp/{name}.torrent',
             'dst_fields': ['name'],
            },
            store_link,
            argenteam_email,
        ],
    'periscope-video': [
            {'name': 'Periscope - Subtitles', 
             'handler': handler.subtitles_periscope,
             'cache_folder': '.cache',
             'langs': ['es'],
            },
            {'name': 'Periscope - Move files',
             'handler': handler.move_files,
             'dst_folder': '/tmp/',
             'fields': ['link', 'subtitle_path']
             },
            {'name': 'Periscope - Notify',
             'handler': handler.send_email,
             'email': email_config,
             'destination': ['destination email'],
             'subject': 'New subtitle download',
             'subject_fields': [],
             'body': '{name} got downloaded.',
             'body_fields': ['name']
             },
        ]
    }
