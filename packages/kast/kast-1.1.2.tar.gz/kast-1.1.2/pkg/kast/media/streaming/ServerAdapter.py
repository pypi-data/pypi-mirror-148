#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J.

import socketserver
import wsgiref.simple_server as wsgi_server
from typing import Optional

import bottle

from kast.utils.Loggable import Loggable


class ServerAdapter(Loggable, bottle.ServerAdapter):

    def __init__(self, host: str, port: int) -> None:
        super().__init__(host=host, port=port)
        self._server: Optional[wsgi_server.WSGIServer] = None

    def run(self, handler: bottle.Bottle) -> None:
        class Server(socketserver.ThreadingMixIn, wsgi_server.WSGIServer):
            pass

        class RequestHandler(Loggable, wsgi_server.WSGIRequestHandler):

            def log_error(self, format, *args) -> None:
                self.log.error(format % args)

            def log_message(self, format, *args) -> None:
                self.log.info(format % args)

        self._server = wsgi_server.make_server(
            host=self.host,
            port=self.port,
            app=handler,
            server_class=Server,
            handler_class=RequestHandler
        )
        self._server.serve_forever()

    def stop(self) -> None:
        self._server.shutdown()
