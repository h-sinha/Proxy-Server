# Proxy Server
HTTP proxy server implemented using python socket programming. Supports Caching, Blacklisting, User Authentication.

## Description
- Proxy runs on port 20100
- Ports 20000 - 200099 are reserved for clients
- Ports 20101 - 20200 are reserved for server
## Features
- Receives the request from client and passes it to the server
- Threaded proxy server thus able to handle many requests at the same time
- The proxy keeps count of the requests that are made. If a URL is requested more than 3 times in 5 minutes, the response from the server is cached. In case of any further requests for the same, the proxy utilises the “If Modified Since” header to check if any updates have been made, and if not, then serves the response from the cache. The cache has a memory limit of 3 responses.
- The proxy supports blacklisting of certain outside domains. These addresses are stored in [proxy_server/blacklist.txt](https://github.com/h-sinha/Proxy-Server/blob/master/proxy_server/blacklist.txt) in CIDR format.
- Proxy authentication is handled using Basic Access Authentication. The authentication is username/password based.
## Requirements
- Python 3
## Instructions for Running
- Start the proxy server 
```
cd proxy_server
python3 server.py
```
