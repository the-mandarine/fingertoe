#!/usr/bin/env python3
import socketserver
import logging
import sys
import os
from glob import glob

HOST, PORT = "", 79
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

PEOPLES = "people"

def init_log(root_log):
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    root_log.addHandler(ch)

class FingerToeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        LOG.info("{} {}".format(self.client_address[0], repr(self.data)))
        self.answer = "No such user"
        people = self.data.decode()
        peoples_path = os.path.join(PEOPLES, '*')
        people_path = os.path.join(PEOPLES, people)
        all_peoples = glob(peoples_path)
        if people_path in all_peoples:
            try:
                with open(people_path, 'r') as people_file:
                    self.answer = people_file.read()
            except:
                pass
        self.request.sendall(self.answer.encode())

class FingerToServer(socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    init_log(LOG)
    server = FingerToServer((HOST, PORT), FingerToeHandler)
    server.serve_forever()

