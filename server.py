import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.close()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    client_socket.send(b'Hello, World!')
    client_socket.close()
