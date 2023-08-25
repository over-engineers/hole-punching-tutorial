import time
import socket

def connect_peer(server_ip, server_port) -> socket.socket:
    # Create socket for server connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Connect to server
    client_socket.connect((server_ip, server_port))
    target_ip_port = client_socket.recv(1024)
    target_ip, target_port = target_ip_port.decode().split(":")
    p2p_socket_port = client_socket.getsockname()[1]
    client_socket.close()

    # Create socket for peer connection
    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
    p2p_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    p2p_socket.bind(("",p2p_socket_port))
    
    # Connect to peer
    for _ in range(5):
        p2p_socket.connect((target_ip, int(target_port)))
        if p2p_socket._closed == False:
            break
        time.sleep(1)
    return p2p_socket


def send_message(socket: socket.socket, message: str):
    socket.sendall(message.encode())
    response = socket.recv(1024).decode()
    print(response)


server_ip = "YOUR STUN SERVER IP"
server_port = 12345 # Port number of STUN server
message = "Hello, Server!"

peer_socket = connect_peer(server_ip, server_port)
send_message(peer_socket, message)
