import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.12', 8080))  # IP is the server IP

for args in sys.argv:
    if args == "":
        args = 'no args'
    else:
        s.send(args + ' ')

print('goodbye!')
