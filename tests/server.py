#!/usr/bin/env python
# encoding: utf-8

from threading import Thread
from wsgiref.simple_server import make_server


def serve_atom(host, port, content):
    """
    Run HTTP server in separate thread on given host and port, serve given
    content as application/atom+xml, handle one request and exit.
    """

    def serve(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'application/atom+xml')]
        start_response(status, headers)
        return content

    def run_server():
        make_server(host, port, serve).handle_request()

    server = Thread(target=run_server)
    server.start()
