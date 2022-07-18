# Universidad de Costa Rica  |  Equipo Layer 8
# Modulo para comunicarse con un cliente

def interact_with_client(socket, client_data):
    '''' Interaction between server responses and client requests '''
    
    condition = True
    while condition:
        condition = socket.recv_request(client_data)