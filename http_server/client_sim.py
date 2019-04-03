import random
import os
import sys
import time
request_type = ['GET', 'POST']
for i in range(20000, 20100):
	pid = os.fork()
	if pid == 0:
		while True:
			cur_type = request_type[random.randint(1, 10) % 2]
			server_port = random.randint(20101, 20200)
			os.system('curl -X %s --local-port %s --proxy http://harsh:pass@0.0.0.0:20100 http://0.0.0.0:%s/cgi-bin/env.cgi'% (cur_type, i, server_port))
			time.sleep(random.randint(1,100))