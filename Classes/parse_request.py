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
    return (dict)

def parse_request(request, method):
    request = request.strip().splitlines()
    data = separate_request(request, method)
    dict = create_dictionary(request, method)
    if data is not None:
        data = parse_data(data)
    return (data, dict)

def get_requesting_file(filepath):
    try:
        requesting_file = filepath[1].lstrip('/')
    except:
        requesting_file = filepath[1]
    try:
        requesting_file = requesting_file.rstrip('?')
    except:
        pass
    return requesting_file