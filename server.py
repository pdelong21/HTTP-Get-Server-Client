# Author: Patrick Delong
# UCID: pgd22
# CS356 section: 002
from socket import *
import os.path
import datetime, time

serverIP = 'localhost' # local ip address
serverPort = 12000
dataLen = 1000000

def get_fn(s):
    new = ""
    b = False
    for i in s:
        if b:
            if i == ' ':
                return new
            else:
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

    for i in list[2]:
        if bool == True:
            date += i
        elif i == ' ':
            bool = True
        else:
            continue
    return date
#create welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))

#server begins listening for TCP requests
serverSocket.listen(1) # listen for incoming requests made by client

print("Server is ready to receive on port: " + str(serverPort))
#loop forever
while True:
    res = ""

    #get todays date
    t1 = datetime.datetime.now(datetime.timezone.utc)
    date = t1.strftime("%a, %d %b %Y %H:%M:%S %Z")

    #waits on accept for incoming requests, new socket created on return
    connectionSocket, address = serverSocket.accept()

    #read bytes from socket
    data = connectionSocket.recv(dataLen).decode()
    print("data from client: \n" + data)

    fname = get_fn(data) # gets the name of the file

    #if file doesn't exist, end immediatly
    if os.path.isfile(fname) != True:
        res += "HTTP/1.1 404 NOT FOUND\r\n"+"Date: " + date + "\r\n"
        connectionSocket.send(res.encode())
        connectionSocket.close()
        continue

    cli_modDate = get_modDate(data)

    #server file mod date
    secs = os.path.getmtime(fname)
    tup = time.gmtime(secs)
    last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n", tup)
    # Check if the file exists then GET if the the last modtime == previous modtime sent by client
    if os.path.isfile(fname) & (cli_modDate != last_mod_time):
        html_code = ""
        res += "HTTP/1.1 200 OK\r\n"+"Date: " + date + "\r\n"
        res += "Last-Modified: " + last_mod_time

        f_handle = open(fname, 'r')
        for line in f_handle:
            html_code += line
        f_handle.close()
        res += "Content-Length: " + str(len(html_code)) + "\r\n"
        res += "Content-Type: text/html; charsetUTF-8\r\n\r\n"
        res += html_code

    # Conditional GET
    if os.path.isfile(fname) & (cli_modDate == last_mod_time):
        html_code = ""
        res += "HTTP/1.1 304 Not Modified\r\n"+"Date: " + date + "\r\n\r\n"






    connectionSocket.send(res.encode())
    connectionSocket.close()
