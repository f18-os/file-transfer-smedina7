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
            
            file = payload.decode()
            
            if os.path.exists(file):
                print("ERROR File already exists... Exiting.")
                framedSend(sock, b"ERROR File already exists... Exiting.", debug)
                #exit if file exists
                sys.exit()
                
            #if it doesnt exist let Client know    
            framedSend(sock, b"Ready", debug)
            #if file doesn't exist then open file
            f = open(payload,"wb")
                                    
            #start receiving and copying file
            print("Copying... " + payload.decode())
            f.write(payload)
            
            framedSend(sock, payload, debug)
                       