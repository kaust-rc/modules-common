import cherrypy
import addlog

@cherrypy.popargs('id', 'mode', 'hostname', 'name', 'path')
class LogServer(object):
    @cherrypy.expose
    def logs(self, id, mode, hostname, name, path):
        try:
            ip_addr = cherrypy.request.headers.get('X-FORWARDED-FOR')
            cherrypy.log("Inserting: {0}, {1}, {2}, {3}, {4}, {5}".format(id, mode, hostname, ip_addr, name, path))
            addlog.insert_data(id, mode, hostname, name, path, ip_addr)
        except Exception:
            cherrypy.log("Error inserting data", traceback=True)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.thread_pool': 10,
                            'log.screen': False,
                            'log.access_file': '/var/tmp/access.log',
                            'log.error_file': '/var/tmp/errors.log'})
    cherrypy.quickstart(LogServer())
