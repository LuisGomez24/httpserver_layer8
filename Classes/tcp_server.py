# Universidad de Costa Rica  |  Equipo Layer 8
# Clase TCPServer para comunicarse con un cliente

import json
import re
import server
import random

from Classes.general_socket import Socket
import Classes.expressions as expressions
import Classes.expression_tree as expression_tree
import parse_request as parser

''' TCP Server for handling a single client '''
class TCPServer(Socket):

    def __init__(self, host, port):
        Socket.__init__(self, host, port)

    def configure_server(self):
        ''' Configure the server '''

        # create TCP socket for server
        self.create_socket()

        # bind server to the address
        self.printwt(f'Binding server to {self.host}:{self.port}...')
        self.sock.bind((self.host, self.port))
        self.printwt(f'Server binded to {self.host}:{self.port}')
    
    def authentic(self, user, passw):
        ''' Get credentials for a given user '''
        
        with open("JSON/users.json", "r") as file:
        
            datas = json.load(file)

            for users in datas["users"]:
                if (user == users["username"] and passw == users["password"]):
                    return (True, users["canWrite"])
        
        return (False, False)
    
    def login_request(self, request):
        ''' Response after authentify user '''
        
        request_json = json.loads(request)
        user = request_json["username"]
        passw = request_json["password"]
    
        validated, can_write = self.authentic(user, passw)
        
        response = '{"type":"login","username":"'+user+'","password":"'+passw+'",'
        if validated: 
            response += '"validated":true,"canWrite":'+str(can_write).lower()+'}'
            self.printwt('Login completed. New client connection...')
        else:
            response += '"validated":false,"canWrite":false}'
            self.printwt('Login request rejected...')
            
        return response
    
    def handle_request(self, request):
        string_list = request.split('\r\n', 1)     # Split request from spaces
        if len(string_list) > 1:
            request  = string_list[1]
            
        head_data = string_list[0].split(' ')
        method = head_data[0]
        requesting_file = parser.get_requesting_file(head_data)
        data, headers = parser.parse_request(request, method)
            
        
    def handle_client(self, client_data):
        ''' Handle the accepted client's requests '''
        
        client_sock, client_address = client_data
        
        try:
            request = self.recv(client_data)
            
            with request:
                self.handle_request(request)
                # client's request
                response = self.login_request(request)
                self.printwt(f'[ REQUEST from {client_address} ]')

                # send response
                self.send(response, client_data)
                response_json = json.loads(response)
                
                if response_json["validated"]:
                    server.interact_with_client(self, client_data)
                
                # get more data and check if client closed the connection
                data_enc = client_sock.recv(1024)
            self.printwt(f'Connection closed by {client_address}')

        except OSError as err:
            self.printwt(err)
        
        except KeyboardInterrupt as err:
            self.printwt('Keyboard Interrupt...')

        finally:
            self.printwt(f'Closing client socket for {client_address}...')
            client_sock.close()
            self.printwt(f'Client socket closed for {client_address}')


    def shutdown_server(self):
        ''' Shutdown the server '''

        self.printwt('Shutting down server...')
        self.sock.close()
    
    def segment_op(self, operation):
        ''' Segmentation of operations in a list '''

        operations = []

        if operation.rfind("sqrt") >= 0:
            operation = operation.replace("sqrt", "&")
            
        operation, dictionary = expressions.change_numbers(operation)

        while(operation != ""):
            if (re.match(".*[()].*", operation)):
                operation, operations = expressions.include_parentheses(operation, operations)
        
        #Cambiar las raices
        toString = " ".join(operations)
        toString = expressions.add_parentheses(toString)
        operations = list(toString.split(" "))
        return operations
    
    def infix_to_posfix(self, response_json):
        ''' Create a expression tree to separate operations '''

        infix = response_json["operation"]
        infix, dict = expressions.change_numbers(infix)
        
        infix = infix.replace('sqrt', '0&')
        infix = list(infix)
        infix = ' '.join(infix)
        rp = expressions.shunting(expressions.get_input(infix))
        postfix = rp[-1][2]
        postfix = postfix.replace(' ', '')
            
        root = expression_tree.construct(postfix)
        final = expression_tree.get_operation(root)
        final = final.replace('0&', '&')
        final = expressions.add_parentheses(final)

        operations = self.segment_op(final)
        operations = ' '.join(operations)
        operations = expressions.return_numbers(operations, dict)
        operations = list(operations.split(' '))
        operations = expressions.remove_parentheses(operations)

        return operations

    def operation(self, response_json, client_data):
        ''' Response to a read/write request'''

        self.printwt('Operation received successfully...')
        if response_json["request"] == "write":
            operations = self.infix_to_posfix(response_json)
            
            iter = 0
            team_id = 88800
            while(len(operations) > 0):
                identifier = random.randint(0,99)+team_id
                for neighbor in self.router.table:
                    router_response = '{"type":"operation","source":"'+self.router.letter+'","destination":"'+neighbor+'","packet":'+str(identifier)+',"order":'+str(iter)+',"operation":"'+operations.pop(0)+'"}'
                    key_neighbor = self.router.table[neighbor][0]
                    self.router.conn_neighbors[key_neighbor].exit_queue.append(router_response)
                    if(len(operations) == 0):
                        break
                iter += 1

        response = '{"type":"'+response_json["request"]+'","operation":"Any","error":false,"result":"Correct"}'
        self.send(response, client_data)
        
    def error(self, client_data):
        ''' Received an error data from client '''
        
        self.printwt('Unknown error...')
        response = '{"type":"error","message":"Unknown error"}'
        self.send(response, client_data)


    def recv_request(self, client_data):
        ''' Handle an request from client'''
        
        request = self.recv(client_data)
        
        if request:
            request_json = json.loads(request)
            type = request_json['type']
            if type == 'request':
                self.operation(request_json, client_data)
                return True
            elif type != 'disconnect':
                self.error(client_data)
        return False
        