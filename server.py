import logging
import logging.config
import cherrypy
import os.path
import addlog

LOG_CONF = {
    'version': 1,

    'formatters': {
        'void': {
            'format': ''
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'cherrypy_access': {
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'void',
            'filename': '/var/tmp/access.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'cherrypy_error': {
            'level':'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'void',
            'filename': '/var/tmp/errors.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO'
        },
        'cherrypy.access': {
            'handlers': ['cherrypy_access'],
            'propagate': False
        },
        'cherrypy.error': {
            'handlers': ['cherrypy_error'],
            'propagate': False
        },
    }
}

@cherrypy.popargs('mode', 'name', 'path', 'hostname', 'id')
class LogServer:
    @cherrypy.expose
    def index(self, mode, name, path, hostname, id):
        cherrypy.log("Inserting: {0}, {1}, {2}, {3}, {4}".format(mode, name, path, hostname, id))
        try:
            addlog.insert_data(id, mode, hostname, name, path)
        except Exception:
            cherrypy.log("Error inserting data", traceback=True)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 80,
                            'server.thread_pool': 10,
                            'log.screen': False,
                            'log.access_file': '',
                            'log.error_file': ''})
    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)
    logging.config.dictConfig(LOG_CONF)
    cherrypy.quickstart(LogServer(), '/logs/')
