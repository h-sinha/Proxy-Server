import socket 
import threading

proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind(('', 20100))
proxy_socket.listen(10)
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
    http_response = forward_request(client_socket, request, http_header['Host'], port )
    client_socket.send(http_response.encode('ascii'))
    client_socket.close()

while True:
    # print proxy_socket.accept()
    client_socket, client_addr = proxy_socket.accept()
    thread = threading.Thread(target = get_request, args = (client_socket, client_addr))
    thread.start()