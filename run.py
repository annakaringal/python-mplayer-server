#!/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import mplayer

HOST = 'localhost'
PORT = 9998

class MPlayerServer(BaseHTTPRequestHandler):

    def init(self):
        self.player = mplayer.Player()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _send_response(self, response):
        self.wfile.write((json.dumps(response)).encode())

    def do_GET(self):
        self._set_headers()
        self._send_response({'status': 'ok'})

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self._send_response({'status': 'ok'})


def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MPlayerServer)
    print('Starting Mplayer server...i')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
