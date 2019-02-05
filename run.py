#!/usr/bin/python

import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import socketserver

HOST = 'localhost'
PORT = 9998
FILE_PATH = os.getcwd() + '/assets/test8.mkv'

class MPlayer():
    def __init__(self):
        self.command = 'mplayer -vfm ffmpeg '

    def play(self, file_path):
        command = self.command + file_path
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE,
                                   preexec_fn=os.setsid)


class MPlayerServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.player = MPlayer()
        super().__init__(*args, **kwargs)

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _send_response(self, response):
        self.wfile.write((json.dumps(response)).encode())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        if self.path != '/play':
            self._set_headers(404)
            return

        self.player.play(FILE_PATH)

        self._send_response({'status': 'ok'})


def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MPlayerServer)
    print('Starting Mplayer server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
