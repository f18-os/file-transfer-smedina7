#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../../lib")      # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('-p', '--put'), 'put', "fileName.txt"),
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug, put  = paramMap["server"], paramMap["usage"], paramMap["debug"], paramMap['put']

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
        sys.exit(1)
    
    #send name of file first to create/copy the same file name
    print("Sending " + clientFile + "...")
    framedSend(s, clientFile.encode(), debug)
    
    f = open(clientFile, "rb")  #open file to start reading and sending
    byte = f.read(100)
    while(byte):
        framedSend(s, byte, debug)
        #if you receive error message from server
        if(framedReceive(s,debug) == b"ERROR File already exists... Exiting."):
            sys.exit(1)
        print("received:", framedReceive(s, debug))
        byte = f.read(100)
            
    #let server know that file has been done transferring
    #framedSend(s, b"Done Transferring File", debug)
    #print("received:", framedReceive(s, debug))
