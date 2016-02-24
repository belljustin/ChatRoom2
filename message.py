import struct
import socket

# MESSAGE STRUCT
# Big Endian >
# username_length (32 bits, unsigned)
# username
# content_length (32 bits, unsigned)
# content (content_length bits, string)

def pack_msg(username, content):
    content_length = len(content)
    username_length = len(username)
    s = struct.Struct('>I %ds I %ds' % (username_length, content_length))
    packed_msg = s.pack(username_length, username, content_length, content)
    return packed_msg

def recieve_msg(sock):
    data = sock.recv(4)
    if data:
        username_size = struct.unpack('>I', data)[0]
        username = struct.unpack('>%ds' % username_size, 
                                sock.recv(username_size))[0] 
        content_size = struct.unpack('>I', sock.recv(4))[0]
        content = struct.unpack('>%ds' % content_size, 
                                sock.recv(content_size))[0]
        return (username, content)
    else:
        raise Exception

def send_msg(sock, username, content):
    msg = pack_msg(username, content)
    sock.send(msg)
