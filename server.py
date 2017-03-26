import cherrypy
import addlog

@cherrypy.popargs('id', 'mode', 'hostname', 'name', 'path')
class LogServer:
    @cherrypy.expose
    def index(self, id, mode, hostname, name, path):
        try:
            cherrypy.log("Inserting: {0}, {1}, {2}, {3}, {4}".format(id, mode, hostname, name, path))
            addlog.insert_data(id, mode, hostname, name, path)
        except Exception:
            cherrypy.log("Error inserting data", traceback=True)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 80,
                            'server.thread_pool': 10,
                            'log.screen': False,
                            'log.access_file': '/var/tmp/access.log',
                            'log.error_file': '/var/tmp/errors.log'})
    cherrypy.quickstart(LogServer())
