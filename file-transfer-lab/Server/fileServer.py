#! /usr/bin/env python3

import sys

sys.path.append("../lib")       # for params

import os, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive
    
##    #create receive file if it doesnt exist
##    if not os.path.exists("receivedFile.txt"):
##        open("receivedFile.txt","w+")
##        #f.close()
        
        
   # f = open("receivedFile.txt","wb")  #keep adding to the file; append until it stops receiving

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            
            if debug:
                print("rec'd: ", payload)
                
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            
            #write to file once it's done receiving
            if b".txt" in payload:
                #save name of file to create/copy file: and later append
                if not os.path.exists(payload):
                    open(payload,"a+")
                #open file once done
                f = open(payload,"ab")
                
            #check if get has been called
##            if b"get:" in payload:
##                with open(clientFile, "rb") as f: #open file to start reading and sending
##                    byte = f.read(100)
##                    while byte != b"":
##                        framedSend(s, byte, debug)
##                        print("received:", framedReceive(s, debug))
##                        byte = f.read(100)
            
                
            f.write(payload)
            print("Copying... " + payload.decode())
            
            payload += b"!"             # make emphatic!
            
            framedSend(sock, payload, debug)
                       
    