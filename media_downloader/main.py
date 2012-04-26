import logging

def main(config):
    '''Main application'''
    logging.debug('debug message')
    logging.info('info message')
    logging.warn('warn message')
    logging.critical('critical message')

#    ACA DEBERIA PREPARAR LAS FUENTES. SE VAN A EJECUTAR EN EL ORDEN EN EL QUE SE
#    AGREGARON EN A CONFIGURACION A LA LISTA DE SOURCES.
#    CADA SOURCE TIENE QUE MANEJAR SU OUTPUT CON UNA APLICACION. DEBERIA TENER LA
#    REFERENCIA A LA APLICACION.
#
#    LAS APLICACIONES SE DEBEN CONFIGURAR POR SEPARADO A LOS SOURCES. UNA
#    APLICACION PUEDE SER USADA POR MAS DE UNA FUENTE.
