import cherrypy

class WebServer(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

if __name__ == '__main__':
    cherrypy.quickstart(WebServer())
