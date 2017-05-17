import socket

HOST = 'localhost'
PORT = 50505
SOCKET = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SOCKET.connect((HOST,PORT))

while True:
    msg = input("Msg input:")
    SOCKET.send(msg.encode())
    response = SOCKET.recv(1024)
    print(response.decode())

SOCKET.close()

"""
PUT;foo;1;INT
GET;foo;;
PUTLIST;bar;a,b,c;LIST
APPEND;bar;d;STRING
GETLIST;bar;;
STATS;;;
INCREMENT;foo;;
DELETE;foo;;
"""
