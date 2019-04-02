import socket 
import threading

proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_socket.bind(('', 20100))
proxy_socket.listen(10)

def get_request(client_socket, client_addr):
    print (client_socket, client_addr)
    request = client_socket.recv(1024)
    print (request)
    http_response = '''HTTP/1.1 200 OK
Content-Type: text/html   
\r\n<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>
'''
    client_socket.send(http_response.encode())
    client_socket.close()

while True:
    # print proxy_socket.accept()
    client_socket, client_addr = proxy_socket.accept()
    thread = threading.Thread(target = get_request, args = (client_socket, client_addr))
    thread.start()
    