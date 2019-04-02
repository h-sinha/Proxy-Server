import socket 
import threading
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind(('', 20100))
proxy_socket.listen(10)

data = []
with open("blacklist.txt", "r") as f:
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i].strip()

def forward_request(client_socket, http_request, server, port):
    proxy_client_socket = socket.socket()
    proxy_client_socket.connect((server, port))
    proxy_client_socket.send(http_request)
    response = []
    while True: 
        print("gm")
        data = proxy_client_socket.recv(1024) 
        print(data)
        if len(data) < 1024:
            response.append(data.decode())
            break
        response.append(data.decode())
    return "".join(response)

def is_Blocked(host):
    for x in data:
        if x in host:
            return True
    return False

def get_request(client_socket, client_addr):
    request = client_socket.recv(1024)
    headers = request.decode('ascii').split('\r\n')
    http_header = {}
    port = 80
    for i in range(len(headers)):
        split_data = headers[i].split(':')
        if split_data[0] == 'Host':
            http_header['Host'] = split_data[1][1:]
            if len(split_data) > 2:
                port = int(split_data[2])
        elif split_data[0] == 'Proxy-Authorization':
            http_header['Proxy-Authorization'] = split_data[1][1:]
    print(headers)
    try:
        print(http_header['Proxy-Authorization'])
        if is_Blocked(http_header['Host']):
            http_response = '''HTTP/1.1 200 OK
\r\nContent-Type: text/html   
\r\n<html>
<body>
<h1>The host you are trying to connect is Blacklisted!</h1>
</body>
</html>
'''
            client_socket.send(http_response.encode('ascii'))
        else:
            http_response = forward_request(client_socket, request, http_header['Host'], port )
            client_socket.send(http_response.encode('ascii'))
    except KeyError as e:
        http_response = '''HTTP/1.1 407 Proxy Authorization Required
\r\nProxy-Authenticate: Basic realm="Secret"
'''
        client_socket.send(http_response.encode('ascii'))
        pass
    client_socket.close()

while True:
    # print proxy_socket.accept()
    client_socket, client_addr = proxy_socket.accept()
    thread = threading.Thread(target = get_request, args = (client_socket, client_addr))
    thread.start()