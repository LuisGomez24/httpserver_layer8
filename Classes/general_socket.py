# Universidad de Costa Rica  |  Equipo Layer 8
# Clase Socket generica para la comunicacion

import socket
from datetime import datetime

''' Class Socket for communication '''
class Socket:
    
    def __init__(self, host, port):
        ''' Constructor '''
        
        self.host = host        # host address
        self.port = port        # host port
        self.sock = None        # connection socket

    def printwt(self, msg):
        ''' Print message with current date and time '''
        
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')

    def create_socket(self):
        ''' Create a socket that uses TCP '''

        self.printwt('Creating connection socket ...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.printwt('Socket created')
        
    def send(self, message, data):
        sock, address = data
        self.printwt(f'[ RESPONSE to {address} ]')
        sock.sendall(message.encode('utf-8'))
                  
    def recv(self, data):
        sock, client_address = data
        data_enc = sock.recv(1024)
        self.printwt(f'[ REQUEST from {client_address} ]')
        return data_enc.decode()
    