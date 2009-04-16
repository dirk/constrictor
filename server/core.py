import socket
from utils import *

host = ''
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow it to reuse (1) addresses (for quicker debugging).
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the host and port.
s.bind((host, port))
s.listen(1)
while 1:
  # Accept a new connection
  sock, addr = s.accept()
  print "Connected"
  # Recieve data with a 0 second timeout.
  data = recv_timeout(sock, 0)
  print data
  sock.sendall("test")
  sock.close()
s.close()