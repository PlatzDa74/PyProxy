import socket
import threading

def handle_client(client_socket):
    # Receive the client's request
    request = client_socket.recv(4096)
    
    # Check if it's an SSH request
    if request.startswith(b'SSH'):
        # Forward to Proxy A
        proxy_a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_a_socket.connect(('proxy_a_address', 22))
        proxy_a_socket.send(request)
        
        # Receive the response from Proxy A
        response_a = proxy_a_socket.recv(4096)
        
        # Send the response back to the client
        client_socket.send(response_a)
        
        # Close the connections
        proxy_a_socket.close()
        client_socket.close()
    else:
        # Forward to Proxy B
        proxy_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_b_socket.connect(('proxy_b_address', 443))
        proxy_b_socket.send(request)
        
        # Receive the response from Proxy B
        response_b = proxy_b_socket.recv(4096)
        
        # Send the response back to the client
        client_socket.send(response_b)
        
        # Close the connections
        proxy_b_socket.close()
        client_socket.close()

def start_proxy_server():
    # Create a socket object
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    proxy_server.bind(('localhost', 8080))
    
    # Start listening for incoming connections
    proxy_server.listen(5)
    
    print('Proxy server started on localhost:8080')
    
    while True:
        # Accept a client connection
        client_socket, client_address = proxy_server.accept()
        
        print('Received connection from:', client_address)
        
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Start the proxy server
start_proxy_server()
