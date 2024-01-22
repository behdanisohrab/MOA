# SPDX-License-Identifier: AGPL-3.0-or-later  # This code is licensed under the AGPL-3.0-or-later license.
# lint: pylint  # The pylint tool is used for linting the code.
# pylint: disable=missing-module-docstring  # The missing-module-docstring warning from pylint is disabled.

from urllib.parse import urlparse  # The urlparse function from the urllib.parse module is imported.

from werkzeug.middleware.proxy_fix import ProxyFix  # The ProxyFix class from the werkzeug.middleware.proxy_fix module is imported.
from werkzeug.serving import WSGIRequestHandler  # The WSGIRequestHandler class from the werkzeug.serving module is imported.

from searx import settings  # The settings from the searx module are imported.

  # Define a class called ReverseProxyPathFix.
class ReverseProxyPathFix:  # This class is a middleware that wraps the application and configures the front-end server to add certain headers.
    '''Wrap the application in this middleware and configure the  # This allows the application to be bound to a URL other than / and to an HTTP scheme that is different than what is used locally.
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is  # The constructor of the class takes a WSGI application as an argument.
    different than what is used locally.
  # The constructor initializes the WSGI application, script name, scheme, and server.
    http://flask.pocoo.org/snippets/35/
  # If a base_url is specified in the settings, these values are given preference over any Flask’s generics.
    In nginx:  # The base_url is parsed and the path, scheme, and netloc are extracted.
    location /myprefix {  # If the script name ends with a slash, the slash is removed to avoid infinite redirect on the index.
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;  # The call method is defined. This method is automatically called when the class instance is called like a function.
        proxy_set_header X-Script-Name /myprefix;  # The script name is retrieved from the environment or from the HTTP_X_SCRIPT_NAME header.
        }  # If the script name exists, it is set in the environment.
  # The path info is retrieved from the environment.
    :param wsgi_app: the WSGI application  # If the path info starts with the script name, the script name is removed from the path info.
    '''
  # The scheme is retrieved from the environment or from the HTTP_X_SCHEME header.
    # pylint: disable=too-few-public-methods  # If the scheme exists, it is set in the environment.

    def __init__(self, wsgi_app):  # The server is retrieved from the environment or from the HTTP_X_FORWARDED_HOST header.
  # If the server exists, it is set in the environment.
        self.wsgi_app = wsgi_app  # The WSGI application is called with the environment and start_response as arguments.
        self.script_name = None
        self.scheme = None  # Define a function called patch_application.
        self.server = None  # This function serves pages with HTTP/1.1.
  # The protocol_version of the WSGIRequestHandler is set to the http_protocol_version specified in the settings.
        if settings['server']['base_url']:  # The WSGI application of the app is patched to handle non-root URLs behind a proxy and WSGI.
  # The WSGI application is wrapped in a ReverseProxyPathFix instance, which is wrapped in a ProxyFix instance.
            # If base_url is specified, then these values from are given
            # preference over any Flask's generics.

            base_url = urlparse(settings['server']['base_url'])
            self.script_name = base_url.path
            if self.script_name.endswith('/'):
                # remove trailing slash to avoid infinite redirect on the index
                # see https://github.com/searx/searx/issues/2729
                self.script_name = self.script_name[:-1]
            self.scheme = base_url.scheme
            self.server = base_url.netloc

    def __call__(self, environ, start_response):
        script_name = self.script_name or environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name) :]

        scheme = self.scheme or environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme

        server = self.server or environ.get('HTTP_X_FORWARDED_HOST', '')
        if server:
            environ['HTTP_HOST'] = server
        return self.wsgi_app(environ, start_response)


def patch_application(app):
    # serve pages with HTTP/1.1
    WSGIRequestHandler.protocol_version = "HTTP/{}".format(settings['server']['http_protocol_version'])
    # patch app to handle non root url-s behind proxy & wsgi
    app.wsgi_app = ReverseProxyPathFix(ProxyFix(app.wsgi_app))
