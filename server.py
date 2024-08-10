import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Confirm socket creation and bind it to the port
try:
    server_socket.bind(('0.0.0.0', 8080))
    print("Socket binded to 0.0.0.0 on port 8080")
except socket.error as msg:
    print(f"Bind failed. Error Code : {str(msg[0])} Message {msg[1]}")
    sys.exit()

server_socket.listen(5)
print("Socket is now listening")

# Main loop to accept connections
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    client_socket.send(b'Hello, World!')
    client_socket.close()
