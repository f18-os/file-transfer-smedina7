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
    )


progname = "fileClient"
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
clientFile = args[len(args)-1] #assuming that name of the file will always be types last

byteL = 100

#check if file exists
if not os.path.exists(clientFile):
    print ("File %s doesn't exist! Exiting" % clientFile)
    exit()

#handling put
    
if "put" in userInput:
    
    with open(clientFile, "rb") as f: #open file to start reading and sending
        byte = f.read(1)
        while byte != b"":
            framedSend(s, byte, debug)
            print("Sending " + clientFile + "...")
            print("received:", framedReceive(s, debug))
            byte = f.read(1)
        
        f.close() #close file once done
        
#handling get
        
if "get" in userInput:
    
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
        
    

          
          

