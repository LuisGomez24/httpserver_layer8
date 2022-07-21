from operator import index
import socket
import json

can_write = False
ind = -1
result = ''

def read(operation):
    try:
        index = int(operation)
        if index == -1:
            index = 'all'
    except:
        index = None
        return ('400 Bad Request', str(index))
    print(index)
    return ('200 OK', str(index))

def create_result(index):
    res = ''
    with open("../JSON/storage.json", "r") as file:
        datas = json.load(file)
        datas.pop('all')
        if index == 'all':
            for key in datas:
                res += '<p>' + datas[key] + '</p>'
                status = '200 OK'
        else:
            try:
                res = '<p>' + datas[index] + '</p>'
                status = '200 OK'
            except:
                res = None
                status = '400 Bad Request'
    return (status, res)

def write(operation):
    pass

# {1: {'operation': '2+5-8', 'result': '-1'}, 2:'6*4/2'}

def login(user, passwd):
    ''' Get credentials for a given user '''
        
    with open("../JSON/users.json", "r") as file:
    
        datas = json.load(file)

        for users in datas["users"]:
            if (user == users["username"] and passwd == users["password"]):
                return ('200 OK', users["canWrite"])
    
    return ('401 Unauthorized', False)

def separate_request(request, method):
    data = None
    if method == 'POST':
        data = request.pop()
        request.pop()           # Extra data 
    return data

def create_dictionary(request, method):
    if method == 'POST':
        dict = {}
        for data in request:
            data_list = data.split(':', 1)
            dict.update({data_list[0]: data_list[1].lstrip()})
    else:
        dict = None
    return dict

def parse_data(data):
    dict = {}
    data = data.split('&')
    for d in data:
        token = d.split('=')
        if len(token) == 1:
            dict.update({token[0]:''})
        else:
            dict.update({token[0]:token[1]})
    return dict

def parse_request(request, method):
    request = request.strip().splitlines()
    data = separate_request(request, method)
    dict = create_dictionary(request, method)
    if data is not None:
        data = parse_data(data)
    return (data, dict)

def choose_data(data):
    try:
        filename = None
        global result
        match data['type']:
            case 'login':
                global can_write
                status, write_op = login(data['user'], data['password'])
                can_write = write_op
                if status == '401 Unauthorized':
                    filename = 'index.html'
                else:
                    filename = 'calculator.html'
            case 'read':
                filename = 'calculator.html'
                status, index = read(data['operation'])
                if status == '400 Bad Request':
                    return (status, filename)
                status, res = create_result(index)
                result = res
            case 'write':
                filename = 'calculator.html'
                status = write(data['operation'])
                res = create_result(index)
                result = res
            case 'exit':
                status = '200 OK'
                filename = 'index.html'
    except:
        filename = 'index_404.html'
    return (status, filename)
 
HOST,PORT = '127.0.0.1',8080
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(10)
 
print('Serving on port ',PORT)
 
while True:
    connection,address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    string_list = request.split('\r\n', 1)     # Split request from spaces
    if len(string_list) > 1:
        request  = string_list[1]      # Request without protocol and method
        
    head_data = string_list[0].split(' ')  # protocol and method
    method = head_data[0]
    print(method)
    try:
        requesting_file = head_data[1].lstrip('/')
    except:
        requesting_file = ''

    try:
        requesting_file = requesting_file.rstrip('?')
    except:
        pass
            
    myfile = requesting_file
    data, headers = parse_request(request, method)
    print(data)
    try:
        print(data['type'])
    except:
        pass
    status = '200 OK'
    
    if method == 'POST':
        status, myfile = choose_data(data)
        if myfile is None:
            myfile = 'index_404.html'
            status = '404 Not Found'
    
    print('status ', status)
        
    if(myfile == ''):
        myfile = 'index.html'    # Load index file as default
 
    try:
        file = open(myfile,'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
        
         
        response = response.decode('utf-8')
        match status:
            case '401 Unauthorized':
                response = response.replace('<!--' , '')
                response = response.replace('-->', '')
            case '400 Bad Request':
                response = response.replace('<!--*' , '')
                response = response.replace('*-->', '')
            case '200 OK':
                try: 
                    if data['type'] == 'read' or data['type'] == 'write':
                        response = response.replace('<!--/' , '')
                        response = response.replace('/-->', '')
                        response =  response.replace('###', result)
                except:
                    pass
        response = response.encode('utf-8')
 
        header = 'HTTP/1.1' + status + '\n'
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
