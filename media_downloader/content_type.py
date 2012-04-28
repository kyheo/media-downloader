TYPE = {'magnet': 'magnet', 
        'torrent': 'torrent'}

class ContentType(object):

    def __init__(self, type_, name, link, extra=None):
        self.type = type_
        self.name = name
        self.link = link
        self.extra = extra
    
    def __repr__(self):
        return '%s - %s' % (self.type, self.name)
