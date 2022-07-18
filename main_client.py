# Universidad de Costa Rica  |  Equipo Layer 8
# Cliente que envia solicitudes

import argparse
import getpass
import json
import re
import sys

from Classes.tcp_client import ClientSocket

BUFFER_SIZE = 128

def parse_arguments():
    ''' Arguments with User and Password'''
    
    parser = argparse.ArgumentParser()
    user = ''; password = ''; port = 0
    if len(sys.argv) > 1:
        parser.add_argument('-u', '--user', help='Username to login', required=True)
        parser.add_argument('-p', '--password', help="Password's user  to login", required=True)
        parser.add_argument('-k', '--port', help="Port's Server", required=True)
        args = parser.parse_args()
        user = args.user
        password = args.password
        port = int(args.port)
    else:
        user = input('Username: ')
        password = getpass.getpass('Password: ')
        port = int(input("Port's Server: "))
        
    return (user, password, port)


def read_op(sock, index):
    ''' Send read operation to server '''
    
    try:
        index = int(index)
        request = '{"type":"request","request":"read","index":'
        if index == -1:
            request += '-1}'
        elif index >= 0:
            request += str(index)+'}'
            
        # Socket Communication
        sock.send(request)
        response = sock.recv()
        response_json = json.loads(response)
        
        if response_json['error']:
            sock.printwt("Operation not found")
        elif not response_json['error']:
            sock.printwt(response_json['operation']+": "+response_json['result'])
        else:
            sock.printwt('An error occured while handling the operation...')
            
    except:
        sock.printwt("Invalid Index. It must be an positive integer or -1...")
        
    return True


def write_op(sock, operation):
    ''' Send write operation to server '''
    
    if sock.can_write:
        raiz = re.compile(r'([\-+*\/^][0-9]|[0-9]|sqrt(.[0-9]))')
        if re.match(raiz, operation):
            request = '{"type":"request","request":"write","operation":"'+str(operation)+'"}'
            sock.send(request)
            
            response = sock.recv()
            response_json = json.loads(response)
            
            if not response_json['error']:
                sock.printwt(response_json['operation']+": "+response_json['result'])
            else:
                sock.printwt('An error occured while handling the operation...')
                
        elif re.match(re.compile(r'sqrt(.[\-+*\/^][0-9])'), operation): 
            sock.printwt("Invalid operation, only positive numbers in square root...")
        else:
            sock.printwt("Invalid operation, please use integer numbers...")
    else:
        sock.printwt("Do not have write permissions...")
    return True


def exit_op(sock, exit):
    ''' Close connection and exit '''
    
    request = '{"type":"disconnect"}'
    sock.send(request)
    return False
  
  
def default_op(sock, default):
    ''' Default Invalid operation '''
    
    sock.printwt("Invalid operation...")
    return True


def do_operation(sock, operation_select):
    ''' Get request type from client input '''
    
    switch_operation = {'-r': read_op, '-w': write_op, '-q': exit_op}
    operation_select = operation_select.replace(' ', '')
    operation = operation_select[:2]
    value = operation_select[2:]
    return switch_operation.get(operation, default_op)(sock, value)


def interact_with_server(sock):
    '''' Interaction between client requests and server responses '''
    
    user, password, port = parse_arguments()
    sock.port = port
    sock.connect()
    validated = sock.login_request(user, password)
    
    while(validated):
        operation_select = input()
        var = do_operation(sock, operation_select)
        if not var:
            break


def main():
    ''' Create a TCP Client and interact with the server at 127.0.0.1:4444 '''
    
    tcp_client = ClientSocket('127.0.0.1', 4444)
    tcp_client.create_socket()
    try:
        interact_with_server(tcp_client)
        
    except OSError as err:
        tcp_client.printwt('Cannot connect to server')
        print(err)
        
    except KeyboardInterrupt as err:
        tcp_client.printwt('Keyboard Interrupt...')

    finally:
        # close socket
        tcp_client.close_socket()


if __name__ == '__main__':
    main()
