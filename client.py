#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys

host = 'localhost'
port = 5006
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
sys.stdout.write('>>')
contentlength = 0
tab = "\t"

while 1:
    # read from keyboard
    line = sys.stdin.readline()
    if line == '\n':
        break
    s.send(line)
    data = s.recv(size)
    print data
    requestheader = line.split(" ")[0]
    if requestheader.lower() == "get" and 'Content-Length' in data:
        contentlength = int(data.split("Content-Length: ")[1].split("\r\n")[0])
        #print contentlength
        datafile =s.recv(contentlength)
        #parse datafile
        ''' pseudocode
        indentasi = 0
        if '<' :
            indentasi += 1
        if '><' :
            while i in indentasi:
                print tag
        if '</' or '/>' :
            indentasi -= 1
        #'''
        #indentasi = 0
        
        print datafile
    
    sys.stdout.write('>>')
    
    #buat nerima perintah yang lebih dari 1024 karakter
    #PROBLEM, gimana caranya client tetep bisa nerima perintah lebih dari 1024 karakter? (selain gag pake size ato sizenya digedein)
    #cara while dibawah salah karena nunggu server ngasih perintah lagi
    '''
    while(data):
        sys.stdout.write(data)
        #data =s.recv(size)
        sys.stdout.write(data)
        if data=='': 
            break
    #'''
s.close()
