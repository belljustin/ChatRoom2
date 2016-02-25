from __future__ import print_function

import socket
import thread
import select
from contextlib import contextmanager

from Tkinter import *

import message
from chatbox import Chatbox

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
    master = Tk()
    master.geometry("300x200+300+300")

    with socketcontext(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        chatbox = Chatbox(master, s)
        thread.start_new_thread(post_listener, (s,chatbox))

        chatbox.pack()
        mainloop()

def post_listener(sock, view):
    while True:
        ready_to_read, ready_to_write, in_error = \
            select.select([sock], [], [])
        for s in ready_to_read:
            try:
                username, msg = message.recieve_msg(s)
                view.write(username, msg)
            except:
                raise Exception
                return

start_client()
