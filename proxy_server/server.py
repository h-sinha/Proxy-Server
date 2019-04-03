import socket 
import _thread
import base64
import threading

proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind(('', 20100))
proxy_socket.listen(10)

data = []
buffer_size = 8192
with open("blacklist.txt", "r") as f:
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip()
creds = []
with open("auth.txt", "r") as f:
    creds = f.readlines()
    for i in range(len(creds)):
        creds[i] = creds[i].strip()
def forward_request(client_socket, http_request, server, port):
    proxy_client_socket = socket.socket()
    proxy_client_socket.settimeout(2)
    proxy_client_socket.connect((server, port))
    proxy_client_socket.send(http_request)
    while True: 
        try:
            data = proxy_client_socket.recv(buffer_size) 
        except socket.timeout:
            break
            pass
        if not data:
            client_socket.send(data)
            break
        client_socket.send(data)
    proxy_client_socket.close()
    return
def is_Blocked(host):
    for x in data:
        if x in host:
            return True
    return False

def auth(credentials):
    y = base64.b64decode(credentials).decode()
    for x in creds:
        if x == y:
            return True
    return False

def get_request(client_socket, client_addr):
    request = client_socket.recv(1024)
    headers = request.decode().split('\r\n')
    http_header = {}
    port = 80
    new_header = []
    for i in range(len(headers)):
        split_data = headers[i].split(':')
        if split_data[0] == 'Host':
            new_header.append(headers[i])
            http_header['Host'] = split_data[1][1:]
            if len(split_data) > 2:
                port = int(split_data[2])
        elif split_data[0] == 'Proxy-Authorization':
            http_header['Proxy-Authorization'] = split_data[1][1:]
        else:
            new_header.append(headers[i])
    try:
        if auth(http_header['Proxy-Authorization'].split(' ')[1]) is False:
            raise Exception
        if is_Blocked(http_header['Host']):
            http_response = '''HTTP/1.1 200 OK
\r\nContent-Type: text/html   
\r\n<html>
<body>
<h1>The host you are trying to connect is Blacklisted!</h1>
</body>
</html>
'''
            client_socket.send(http_response.encode())
        else:
            forward_request(client_socket, "\r\n".join(new_header).encode(), http_header['Host'], port)
    except Exception as e:
        print(e)
        http_response = '''HTTP/1.1 407 Proxy Authorization Required
Content-Type: text/html
Proxy-Authenticate: Basic realm="Secret"
\r\n<html>
<body>
<h1>Please Authenticate!</h1>
</body>
</html>
'''
        client_socket.send(http_response.encode())
        pass
    client_socket.close()

while True:
    threading.enumerate()
    (client_socket, client_addr) = proxy_socket.accept()
    thread = threading.Thread(target = get_request, args = (client_socket, client_addr))
    thread.setDaemon(True)
    thread.start()
