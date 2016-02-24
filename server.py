import sys
import socket
import thread
import select
import logging
from contextlib import contextmanager
from Queue import Queue

import message

logging.basicConfig(filename="log_server.log",level=logging.DEBUG, format='%(asctime)s %(message)s')

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

HOST = '127.0.0.1'
PORT = 50007

connected_sockets = list()
message_queue = Queue()

@contextmanager
def socketcontext(*args, **kw):
    s = socket.socket(*args, **kw)
    try:
        yield s
    finally:
        s.close()

def accept_connection(server):
    conn, addr = server.accept()
    connected_sockets.append(conn)
    logging.info('Connected by ' + str(addr))

def broadcast_messages(server):
    while not message_queue.empty():
        username, content = message_queue.get()
        for s in connected_sockets:
            if s != server:
                message.send_msg(s, username, content)

def serve_chat():
    with socketcontext(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(10)
        connected_sockets.append(server)
        while True:
            ready_to_read, ready_to_write, in_error = \
            select.select(connected_sockets, [], [])
            for s in ready_to_read:
                if s is server:
                    accept_connection(s)
                else:
                    try:
                        msg = message.recieve_msg(s)
                        message_queue.put(msg)
                        logging.info("Msg recieved from: " + msg[0])
                    except:
                        connected_sockets.remove(s)
                        logging.info("Disconnected from: " + str(s))
            broadcast_messages(server)

serve_chat()
