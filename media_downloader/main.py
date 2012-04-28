import logging
import source

def main(config):
    '''Main application'''
    logging.info('Start')
    try:
        source_manager = source.Manager(config.SOURCES)
        content = source_manager.fetch_content()
        print content
    except Exception, e:
        logging.exception(e)
        return
    logging.info('End')
