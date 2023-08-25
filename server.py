from datetime import datetime
import socket
from typing import Tuple


def start_stun_server(ip, port):
    first_session: Tuple[str, int, socket.socket] = None
    second_session: Tuple[str, int, socket.socket] = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    s.bind((ip, port))
    s.listen(2)
    print(f"[*] Listening on {ip}:{port}")

    try:
        while True:
            conn, addr = s.accept() #-> connect 
            print(f"[*] Accepted connection from: {addr[0]}:{addr[1]} at {datetime.now()}")

            if first_session is None:
                first_session = (addr[0], addr[1], conn)
            else:
                second_session = (addr[0], addr[1], conn)

                first_session[2].send(f"{second_session[0]}:{second_session[1]}".encode('utf-8'))
                second_session[2].send(f"{first_session[0]}:{first_session[1]}".encode('utf-8'))

                first_session[2].close()
                second_session[2].close()

                first_session = None
                second_session = None
                
    except KeyboardInterrupt:
        print("\n[*] Shutting down the server...")
        s.close()


if __name__ == '__main__':
    HOST_IP = '0.0.0.0'
    HOST_PORT = 12345 # Port number of STUN server

    start_stun_server(HOST_IP, HOST_PORT)
