import socket
import threading
import select

# Proxy server settings
PROXY_HOST = '127.0.0.1'  # Proxy server IP address
PROXY_PORT = 8888  # Proxy server port

# SSH server settings
SSH_HOST = 'raspi1.fritz.box'  # SSH server IP address or hostname
SSH_PORT = 22  # SSH server port

# HTTPS server settings
HTTPS_HOST = 'raspi1.fritz.box'  # HTTPS server IP address or hostname
HTTPS_PORT = 443  # HTTPS server port

# Function to handle SSH client connections
def handle_ssh_client(client_socket):
    ssh_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh_server_socket.connect((SSH_HOST, SSH_PORT))

    while True:
        r, _, _ = select.select([client_socket, ssh_server_socket], [], [])
        if client_socket in r:
            data = client_socket.recv(4096)
            if len(data) == 0:
                break
            ssh_server_socket.sendall(data)

        if ssh_server_socket in r:
            data = ssh_server_socket.recv(4096)
            if len(data) == 0:
                break
            client_socket.sendall(data)

    client_socket.close()
    ssh_server_socket.close()

# Function to handle HTTPS client connections
def handle_https_client(client_socket):
    https_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    https_server_socket.connect((HTTPS_HOST, HTTPS_PORT))

    while True:
        r, _, _ = select.select([client_socket, https_server_socket], [], [])
        if client_socket in r:
            data = client_socket.recv(4096)
            if len(data) == 0:
                break
            https_server_socket.sendall(data)

        if https_server_socket in r:
            data = https_server_socket.recv(4096)
            if len(data) == 0:
                break
            client_socket.sendall(data)

    client_socket.close()
    https_server_socket.close()

# Main proxy server function
def proxy_server():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(10)

    print(f"Proxy server started on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Determine the client type based on the first byte of the handshake
        first_byte = client_socket.recv(1)
        client_socket.close()

        if first_byte == b'\x16':  # SSL/TLS handshake starts with 0x16
            threading.Thread(target=handle_https_client, args=(client_socket,)).start()
        else:
            threading.Thread(target=handle_ssh_client, args=(client_socket,)).start()

    proxy_socket.close()

# Start the proxy server
proxy_server()
