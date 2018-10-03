#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-p', '--put'), 'put', "fileDoesNotExist.txt"),
    (('-g', '--get'), 'get', "fileDoesNotExist.txt"),
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug, put, get  = paramMap["server"], paramMap["usage"], paramMap["debug"], paramMap['put'], paramMap['get']

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

#handling put  
if put:
    
    #store name of file
    split = re.split('put', put)
    clientFile = split[0]
    #check if file exists first
    if not os.path.exists(clientFile):
        print ("File %s doesn't exist! Exiting" % clientFile)
        exit()
    
    #send name of file first to create/copy the same file name
    #framedSend(s, clientFile, debug)
    
    with open(clientFile, "rb") as f: #open file to start reading and sending
        byte = f.read(100)
        while byte != b"":
            framedSend(s, byte, debug)
            print("Sending " + clientFile + "...")
            print("received:", framedReceive(s, debug))
            byte = f.read(100)
        
        f.close() #close file once done
        
#handling get       
if get:
    
    if not os.path.exists("receivedFile.txt"):
        open("receivedFile.txt","w+")
    
    with open(clientFile, "rb") as f:       
        while True:
            payload = framedReceive(s, debug)
            
            if debug:
                print("rec'd: ", payload)
                
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            
            #write to file once it's done receiving
            f.write(payload)
            print("Copying... " + payload.decode())
            
            payload += b"!"             # make emphatic!
            
            framedSend(sock, payload, debug)
