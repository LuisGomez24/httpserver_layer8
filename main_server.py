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
    
    # Create thread to calculate operations
    r_thread = threading.Thread(target = server.calculate_system())
    r_thread.daemon = True
    r_thread.start()
    print("Calculate Thread created...")
    

def main(ip, port, node):
    ''' Create a TCP Server and handle multiple clients simultaneously '''

    tcp_server_multi_client = ReceptionSocket(ip, port)
    tcp_server_multi_client.configure_server(node)
    create_threads_server(tcp_server_multi_client)

if __name__ == '__main__':
    port = 4000 + ord(sys.argv[2]) - ord('A')
    main(sys.argv[1], port, sys.argv[2])
