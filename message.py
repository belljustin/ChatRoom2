import struct
import socket

# MESSAGE STRUCT
# Big Endian >
# content_length (32 bits, unsigned)
# content (content_length bits, string)

def pack_msg(content):
    content_length = len(content)
    s = struct.Struct('I %ds' % content_length)
    packed_msg = s.pack(content_length, content)
    return packed_msg

def recieve_msg(sock):
    data = sock.recv(4)
    if data:
        content_size = struct.unpack('I', data)[0]
        content = struct.unpack('%ds' % content_size, sock.recv(content_size))[0]
        return (content_size, content)
    else:
        raise Exception

def send_msg(sock, content):
    msg = pack_msg(content)
    sock.send(msg)
