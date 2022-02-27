import cherrypy

_CHERRYPY_CONFIG = { 
    'global': {
        'server.socket_port': 80,
    }
}
_ROOT = './webserver/www/'
_STATIC_PAGES = {
    'index': 'login.html'
}


class WebServer(object):
    @cherrypy.expose
    def resources(self):
        pass  # Not sure what to do here

    @cherrypy.expose
    def index(self):
        with open(_ROOT + _STATIC_PAGES['index']) as file:
            page = file.readlines()
            return page


def start_service():
    cherrypy.config.update(_CHERRYPY_CONFIG)
    cherrypy.quickstart(WebServer())


if __name__ == '__main__':
    start_service()
