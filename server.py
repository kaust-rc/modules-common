import cherrypy
import addlog

@cherrypy.popargs('mode', 'name', 'path', 'hostname', 'id')
class LogServer(object):
    @cherrypy.expose
    def index(self, mode, name, path, hostname, id):
        addlog.insert_data(id, mode, hostname, name, path)

cherrypy.config.update({'log.screen': False,
                        'log.access_file': '/var/tmp/module.logs.access',
                        'log.error_file': '/var/tmp/module.logs.err',})

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8887,})

cherrypy.quickstart(LogServer(), '/logs/')
