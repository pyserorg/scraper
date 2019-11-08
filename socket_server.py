import socket
import sys
import time

server_address = './sample_socket'

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

sock.connect(server_address)

message = 'ALO!'
while True:
    sock.sendall(message.encode('ascii'))
    print('ALO!')

    # Clean up the connection
    time.sleep(3)
    sock.close()
