# Author: Patrick Delong
# UCID: pgd22
# CS356 section: 002
import sys
from socket import *

def get_host(s):
    new = ""
    for i in s:
        if i == ':':
            return new
        else:
            new += i
def get_port(s):
    new = ""
    for i in s:
        if i.isdigit():
            new += i
        else:
            continue
    return int(new)

def get_fn(s):
    new = ""
    b = False
    for i in s:
        if b:
            new += i
        elif i == '/':
            b = True
        else:
            continue
    return new
def get_modDate(s):
    date = ""
    list = []
    temp = ""
    bool = False
    for i in s:
        if i == '\n':
            temp += i
            list += [temp]
            temp = ""
        else:
            temp += i
    if len(list) >=3:
        for i in list[2]:
            if bool == True:
                date += i
            elif i == ' ':
                bool = True
            else:
                continue
    return date


url = sys.argv[1] # cmd line arg
host = get_host(url) # grabs hostname from arg
port = get_port(url) # grabs port number from arg
fname = get_fn(url) # grabs file name from arg
dataLen = 1000000

# Regular GET
clientSocket = socket(AF_INET, SOCK_STREAM)
cli_get = "GET /" + fname + " HTTP/1.1\r\nHost: " + host + ":" + str(port) + "\r\n\r\n"
print("Connecting to server")
clientSocket.connect((host,port))

clientSocket.send(cli_get.encode())

res_echo = clientSocket.recv(dataLen)
print(res_echo.decode())
clientSocket.close()

# Extract the modified date from previous response & Condtional GET
modDate = get_modDate(res_echo.decode())
clientSocket = socket(AF_INET, SOCK_STREAM)
cli_condGet = "GET /" + fname + " HTTP/1.1\r\nHost: " + host + ":" + str(port) + "\r\nIf-Modified-Since: " + modDate + "\r\n"
clientSocket.connect((host,port))
clientSocket.send(cli_condGet.encode())

cond_resEcho = clientSocket.recv(dataLen)
print(cond_resEcho.decode())
clientSocket.close()
