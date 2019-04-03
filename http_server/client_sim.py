import random
import os
port = random.randint(20000, 20099)
request_type = ['GET', 'POST']
f = 1
while f:
	cur_type = request_type[random.randint(1, 10) % 2]
	server_port = random.randint(20101, 20200)
	os.system('curl -X %s --local-port %s --proxy http://admin:admin@0.0.0.0:20100 http://0.0.0.0:20196/cgi-bin/env.cgi'% (cur_type, port))
	f = 0