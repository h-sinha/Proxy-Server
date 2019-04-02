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

def is_Blocked(host):
    for x in data:
        if x in host:
            return True
    return False

def get_request(client_socket, client_addr):
    # print (client_socket, client_addr)
    request = client_socket.recv(1024)
    print(request)
    headers = request.decode('ascii').split('\r\n')
    http_header = {}
    for i in range(len(headers)):
        split_data = headers[i].split(':')
        if split_data[0] == 'Host':
            http_header['Host'] = split_data[1][1:]
    print(http_header['Host'])
    if is_Blocked(http_header['Host']):
        http_response = '''HTTP/1.1 200 OK
Content-Type: text/html   
\r\n<html>
<body>
<h1>The host you are trying to connect is Blacklisted!</h1>
</body>
</html>
'''
        client_socket.send(http_response.encode('ascii'))
        client_socket.close()
    http_response = '''HTTP/1.1 200 OK
Content-Type: text/html   
\r\n<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>
'''
    client_socket.send(http_response.encode('ascii'))
    client_socket.close()

while True:
    # print proxy_socket.accept()
    client_socket, client_addr = proxy_socket.accept()
    thread = threading.Thread(target = get_request, args = (client_socket, client_addr))
    thread.start()