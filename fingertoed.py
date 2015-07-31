#!/usr/bin/env python3
import socketserver
import logging
import sys
import os
from glob import glob

HOST, PORT = "", 7979
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

PEOPLES = "/share/%s/finger/"
DESC_FILE = "desc"
PLAN_FILE = "plan"

def init_log(root_log):
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    root_log.addHandler(ch)

def get_file(fpath, all_paths, error=None):
    answer = ""
    if fpath in all_paths:
        try:
            with open(fpath, 'r') as people_file:
                answer += people_file.read()
        except:
            pass
    else:
        if error is not None:
            answer = error
    return answer

class FingerToeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        LOG.info("{} - {}".format(self.client_address[0], repr(self.data)))
        self.answer = ""
        people = self.data.decode()
        peoples_path = os.path.join(PEOPLES % ('*'), '*')
        desc_path = os.path.join(PEOPLES % (people), DESC_FILE)
        plan_path = os.path.join(PEOPLES % (people), PLAN_FILE)
        all_peoples = glob(peoples_path)
        self.answer += get_file(desc_path, all_peoples, "No such user.")
        self.answer += get_file(plan_path, all_peoples, "No Plan.")
        if not people:
            self.answer = "Must provide username"
        self.request.sendall(self.answer.encode())

class FingerToServer(socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

if __name__ == "__main__":
    init_log(LOG)
    server = FingerToServer((HOST, PORT), FingerToeHandler)
    server.serve_forever()

