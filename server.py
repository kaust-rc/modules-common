import cherrypy, os.path, addlog

@cherrypy.popargs('mode', 'name', 'path', 'hostname', 'id')
class LogServer:
    @cherrypy.expose
    def index(self, mode, name, path, hostname, id):
        try:
            addlog.insert_data(id, mode, hostname, name, path)
        except Exception:
            cherrypy.log("Error inserting data", traceback=True)


conf = os.path.join(os.path.dirname(__file__), 'server.conf')
cherrypy.quickstart(LogServer(), '/logs/', config=conf)
