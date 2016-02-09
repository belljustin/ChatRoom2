from __future__ import print_function

import socket
import thread
import select
from contextlib import contextmanager

import message

HOST = '127.0.0.1'
PORT = 50007

@contextmanager
def socketcontext(*args, **kw):
    s = socket.socket(*args, **kw)
    try:
        yield s
    finally:
        s.close()

def start_client():
    with socketcontext(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        thread.start_new_thread(post_listener, (s,))
        while True:
            msg = raw_input()
            message.send_msg(s, msg)

def post_listener(sock):
    while True:
        ready_to_read, ready_to_write, in_error = \
            select.select([sock], [], [])
        for s in ready_to_read:
            try:
                msg = message.recieve_msg(s)[1]
                print("\r" + msg, end="\n")
            except:
                print("\rConnection with server was lost")
                raise Exception
                return

start_client()
