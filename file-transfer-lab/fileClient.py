#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

#open file to send it to server

#STORE the name of the file that user wants to send
userInput = input("Type in command: ")
args = userInput.split(" ")  #store in input as list
clientFile = args[len(args)-1] #nassuming that ame of the file will always be types last
byteL = 100

#check if file exists
if not os.path.exists(clientFile):
    print ("File %s doesn't exist! Exiting" % outputFname)
    exit()
    
##f = open("test.txt",'a')
###seek end of file to append ':' to indicate end of "message" transfer
##f.seek(2) # end of file
##f.write(':')
##f.close()

#handling put
if "put" in clientFile:
    
    f = open(clientFile, "rb")  #open file to start reading and sending
    try:
        byte = f.read(100)
        
    while byte != "":
        framedSend(s, byte, debug)  #send byte at a time
        byte = f.read(100)
        
    finally:
    f.close()
    
    

### attempt to open file to start sending to server
##with open("test.txt", 'r') as rFile:
##    for line in rFile:
##        #1 indicates the current position
## #       sendBytes = rFile.seek(1,2)  #get the contents from the current position until 100 bytes for limit
##        framedSend(s, rFile.read(100), debug)  #send
##        
##        print("received:", framedReceive(s, debug))

