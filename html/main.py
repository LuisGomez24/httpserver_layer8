import socket

def get_head(conn):
    """ gets headers from client """
    data = b''
    while not data.endswith(b"\r\n\r\n"):
        data += conn.recv(1)
    return data

def get_body(conn):
    """ gets the data from client """
    data = b''
    while b'\r\n\r\n' not in data:
        data += conn.recv(1024)
    return data
 
HOST,PORT = '127.0.0.1',8080
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(10)
 
print('Serving on port ',PORT)
 
while True:
    connection,address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    print(request)
    string_list = request.split('\r\n', 1)     # Split request from spaces
    head_data = string_list[0].split(' ')
    requesting_file = ''
    
    try:
        method = head_data[0]
        print(method)
        requesting_file = head_data[1]
        print(requesting_file)
        myfile = '' 
    except IndexError:
        myfile = 'index_400.html' 

    #print('Client request ',requesting_file)
    
    if myfile != 'index_400.html' and requesting_file:
        myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here
        myfile = myfile.lstrip('/')
        
    if(myfile == ''):
        myfile = 'index.html'    # Load index file as default
 
    try:
        file = open(myfile,'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
 
        header = 'HTTP/1.1 200 OK\n'
        if(myfile.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'
 
        header += 'Content-Type: '+str(mimetype)+'\n\n'
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        file = open("index_404.html",'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
 
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
