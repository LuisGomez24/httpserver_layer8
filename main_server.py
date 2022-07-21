# Universidad de Costa Rica  |  Equipo Layer 8
# Server TCP para multiples conexiones

import sys
import threading

from Classes.tcp_server_multi_client import ReceptionSocket

def create_threads_server(server):
    ''' Create a thread to listen requests and a thread to calculate operations '''
    # Create thread to wait clients 
    s_thread = threading.Thread(target = server.wait_for_client())
    s_thread.daemon = True
    s_thread.start()
    print("Clients Thread created...")

def main(port=8080):
    ''' Create a TCP Server and handle multiple clients simultaneously '''

    tcp_server_multi_client = ReceptionSocket('127.0.0.1', port)
    tcp_server_multi_client.configure_server()
    create_threads_server(tcp_server_multi_client)

if __name__ == '__main__':
    main()
