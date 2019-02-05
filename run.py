#!/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import mplayer

HOST = 'localhost'
PORT = 9998
FILE_PATH = './assets/test8.mkv'

class MPlayerServer(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _send_response(self, response):
        self.wfile.write((json.dumps(response)).encode())

    def _create_player(self):
        player = mplayer.Player()
        player.fullscreen = True
        return player

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        if self.path != '/play':
            self._set_headers(404)
            return

        player = self._create_player()
        player.loadfile(FILE_PATH)

        self._send_response({'status': 'ok'})


def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MPlayerServer)
    print('Starting Mplayer server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
