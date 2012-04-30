TYPE = {'magnet': 'magnet', 
        'torrent': 'torrent'}

def create(type_, name, link, extra=None):
    return {'type': type_,
            'name': name,
            'link': link,
            'extra': extra}
