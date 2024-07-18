import socket

host = 'localhost'
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print(f"Listening on {host}:{port}")
conn, addr = s.accept()
print(f"Connected by {addr}")
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)
conn.close()
