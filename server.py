import cherrypy, os.path, addlog

@cherrypy.popargs('mode', 'name', 'path', 'hostname', 'id')
class LogServer:
    @cherrypy.expose
    def index(self, mode, name, path, hostname, id):
        cherrypy.log(mode)
        cherrypy.log(name)
        cherrypy.log(path)
        cherrypy.log(hostname)
        cherrypy.log(id)
        addlog.insert_data(id, mode, hostname, name, path)

conf = os.path.join(os.path.dirname(__file__), 'server.conf')
cherrypy.quickstart(LogServer(), '/logs/', config=conf)
