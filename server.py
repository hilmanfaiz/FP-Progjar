#!/usr/bin/env python
#http://ilab.cs.byu.edu/python/threadingmodule.html 
import select
import socket
import sys
import threading
import os
import datetime
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5006
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)
        
    def run(self):
        self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            read_ready,write_ready,exception = select.select(input,[],[])

            for s in read_ready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                    print "new client connected: ", c, 

                elif s == sys.stdin:
                    print "junk"
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()
        print "Server closed"

class Client(threading.Thread): #, BaseHTTPRequestHandler):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.path = os.path.dirname(os.path.abspath(__file__))+'/halamanWeb/'
        self.pathdefault = os.path.dirname(os.path.abspath(__file__))+'/halamanWeb/' #jangan diubah2 di bawah yaa
        self.requestHeader = ""
        self.filesize = 0
        self.header = ""
        self.data = ""
    
    def sendFile(self):
        #file = open(self.path,"r")
        # trus....
        file = open(self.path,"r")
        data = file.read()
        print data
        self.client.send(data)
        file.close()
            
        
    def sendHeader(self):
        ekstensi = self.path.split('.')[1]
        #.split('\n')[0]
        #print ekstensi
        if (ekstensi == "html"):
            #print "extensi == html" #debugging, monggo hapus
            #print self.path
            try:
                file1 = open(self.path,"r")
                data=file1.read()
                file1.close()
                #print data 
                now = datetime.datetime.now() #tanggal sekarang
                detilnow = now.strftime("%a, %d %b %Y %H:%M:%S")
                versipython= '.'.join(str(i) for i in sys.version_info) #print versipython
                self.filesize=os.path.getsize(self.path)
                #self.client.send("HTTP/1.1 200 OK\r\n") #jek ngawur versi httpnya
                self.header = ""
                self.header += "HTTP/1.1 200 OK\r\n"
                
                #self.client.send("Date: " + detilnow + " GMT\r\n")
                self.header += "Date: " + detilnow + " GMT\r\n"
                
                #self.client.send("Server: " + versipython + "\r\n") #btw server bukannya apache ya?
                self.header += "Server: " + versipython + "\r\n"
                
                #last modified
                self.filelastmod=time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime(self.path)))
                self.header += "Last Modified: "+ str(self.filelastmod) + "\r\n"
                
                #self.client.send("Content-Length: " + str(filesize) + "\r\n")
                self.header += "Content-Length: " + str(self.filesize) + "\r\n"
                
                if 'charset' in data:
                    charset=data.split('charset=')[1].split('"')[0]
                #self.client.send("Content-Type: text/html" + "; charset= " + charset +  "\r\n")
                self.header += "Content-Type: text/html" + "; charset= " + charset +  "\r\n"
                
                #self.client.send("\r\n")
                self.header += "\r\n"
                
                self.client.send(self.header)
                print self.header
                #return 0
                
                #print ukuran
            except IOError:
                print "unknown error code: 1"
                #return 1
            #return 0
    def do_GET_HEAD(self):
        
        ### SiteMap dengan DICTIONARY ###
        # declare dictionary
        sitemap = {}
        
        #fill dictionary
        # 0 = masih ada
        # 1 = uda ga ada / moved permanently
        # 2 = forbidden
        # 3 = internal server error
        sitemap[self.pathdefault+'index.html'] = 1
        sitemap[self.pathdefault+'home.html'] = 0
        sitemap[self.pathdefault+'servererror.html'] = 3
        sitemap[self.pathdefault] = 2
        ### end ###
        
        #versi 3
        #lokasi = os.path.dirname(os.path.abspath(__file__))
        #print lokasi
        #print
        print self.path
        try:
            siteflag = sitemap[self.path]
        
        except KeyError:
            print "404 Not Found"
            self.client.send("404 Not Found\n")
            #return 404
        
        #print siteflag
        
        #'''
        # jika file ada dan boleh diakses
        if siteflag == 0 :
            #print "file found"
            self.sendHeader()
            #print "header sent"
            #print self.requestHeader
            #'''
            if self.requestHeader == "get" :
                print "sending " + str(self.filesize) + " byte(s)..."
                f = open(self.path, 'r')
                self.data = f.read() 
                f.close()
                self.client.send(self.data)
                '''
                file = open(self.path,"r")
                self.data = file.read(self.size)
                while(self.data):
                    self.client.send(self.data)
                    self.data = file.read(self.size)
                    #print self.data
                    if self.data=='': 
                        print "EOF"
                        break
                #self.client.send("\r\n\r\n")                    
                file.close()
                #'''
                print "sending complete..."
            #'''
            #print "file sent"
            #return 200
        # jika file uda dihapus
        if siteflag == 1 :
            print "301 Moved Permanently\n"
            self.client.send("HTTP/1.1 301 Moved Permanently\nContent-Type: text/html;\r\n\r\n")
            #return 301
        # jika file tidak boleh diakses
        if siteflag == 2 :
            print "403 Forbidden\n"
            self.client.send("HTTP/1.1 403 Forbidden\nContent-Type: text/html;\r\n\r\n")
            #return 403
        if siteflag == 3:
            print "500 Internal Server Error\n"
            self.client.send("HTTP/1.1 500 Internal Server Error\nContent-Type: text/html;\r\n\r\n")
            #return 500
        #'''
        
    def do_POST(self):
        self.client.send("HTTP/1.1 200 OK\nContent-Type: text/html;\r\n\r\n")
        
    
    def run(self):
        running = 1
        while running:
            try:
                data = self.client.recv(self.size)
            except:
                self.client.close()
                running = 0
            print 'recv: ', self.address, data # buat debugging
            # Ngoding dari sini
            
            # parsing
            if data:
                self.requestHeader = ""
                self.requestHeader = data.split(" ")[0]
                str1 = self.requestHeader
                self.requestHeader = str1.lower()
                reqfile = data.split("/")[1].split("\n")[0]
                #reqfile = data.split(" ")[1].split("\n")[0]
                #elif requestHeader == GET:
                if (self.requestHeader == "get" or self.requestHeader == "head" ):
                    self.path = self.pathdefault + reqfile
                    #print self.path
                    self.do_GET_HEAD()
                    #self.client.send(data)
                elif(self.requestHeader == "post"):
                    self.path = self.pathdefault + reqfile
                    self.do_POST()
            #elif requestHeader == HEAD:
                
            #elif requestHeader == POST:
            
            # Ngoding sampai sini
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    s = Server()
    s.run()
