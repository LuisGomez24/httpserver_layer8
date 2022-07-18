import socket
 
HOST,PORT = '127.0.0.1',8080
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)
 
print('Serving on port ',PORT)
 
while True:
    connection,address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    print(request)
    string_list = request.split(' ')     # Split request from spaces
 
    try:
        method = string_list[0]
        requesting_file = string_list[1]
        myfile = '' 
    except IndexError:
        myfile = 'index-400.html'

 
    print('Client request ',requesting_file)
    
    if myfile != 'index-400.html':
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
        file = open("index-404.html",'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
 
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
