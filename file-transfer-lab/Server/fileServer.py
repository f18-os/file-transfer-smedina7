#! /usr/bin/env python3

import sys

sys.path.append("../../lib")    # for params

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
            #the first receive will be file name
            file = payload.decode()
            
            #check if file exists with server
            if os.path.exists(file):
                print("ERROR File already exists... Exiting.")
                framedSend(sock, b"ERROR File already exists... Exiting.", debug)
                #exit if file exists
                sys.exit(1)                      
            
            #if file doesn't exist then open file
            f = open(file,"wb")
            
            #start receiving and copying file
            copy = framedReceive(sock, debug)
            print("Copying... " + copy.decode())
            f.write(copy)
            framedSend(sock, payload, debug)
                       
    
