# Universidad de Costa Rica  |  Equipo Layer 8
# Clase ClientSocket para el cliente

import json
from Classes.general_socket import Socket

''' TCP Client to connect with TCP Server '''
class ClientSocket(Socket):

    def __init__(self, host, port):
        ''' Constructor '''
        
        Socket.__init__(self, host, port)
        self.can_write = None
        
    def close_socket(self):
        self.printwt('Closing connection socket...')
        self.sock.close()
        self.printwt('Socket closed')
        
    def connect(self):
        ''' Connect and interact with a TCP Server. '''

        self.printwt(f'Connecting to server [{self.host}] on port [{self.port}] ...')
        self.sock.connect((self.host, self.port))
        self.printwt('Connection completed successfully...')
        
    def login_request(self, user, password):
        
        # send login request
        request = '{"type":"login","username":"'+user+'","password":"'+password+'"}'
        self.printwt('Sending login to server to authenticate...')
        self.send(request)

        # receive login response
        response = self.recv()
        response_json = json.loads(response)
        
        if response_json["validated"]:
            self.printwt('Login completed successfully...')
            self.can_write = response_json["canWrite"]
        else:
            self.printwt('Login failed. User or Password incorrect...')
            
        return response_json["validated"]
