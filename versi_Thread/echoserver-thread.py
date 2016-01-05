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
        self.port = 5002
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

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread): #, BaseHTTPRequestHandler):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.path = '/home/ubuntu/workspace/halamanWeb/'
        self.pathdefault = '/home/ubuntu/workspace/halamanWeb/' #jangan diubah2 di bawah yaa
    
    def sendFile(self):
        file = open(self.path,"r")
        # trus....
    def sendHeader(self):
        ekstensi = self.path.split('.')[1]
        #.split('\n')[0]
        print ekstensi
        if (ekstensi == "html"):
            print "extensi == html" #debugging, monggo hapus
            #print self.path
            try:
                #file = open(self.path,"r")
                now = datetime.datetime.now() #tanggal sekarang
                detilnow = now.strftime("%a, %d %b %Y %H:%M:%S")
                versipython= '.'.join(str(i) for i in sys.version_info)
                print versipython
                self.client.send("HTTP/1.1 200 OK\r\n") #jek ngawur versi httpnya
                self.client.send("Date : " + detilnow + " GMT\r\n")
                self.client.send("Server: " + versipython + "\r\n") #btw server bukannya apache ya? seharusnya iya, tapi kudu njalanin apache berarti
                self.client.send("\r\n")
                #print ukuran
            except IOError:
                print "unknown error code: 1"
                
    def do_GET_HEAD(self):
        
        ### SiteMap dengan DICTIONARY ###
        # declare dictionary
        sitemap = {}
        
        #fill dictionary
        # 0 = masih ada
        # 1 = uda ga ada / moved permanently
        # 2 = forbidden
        sitemap[self.pathdefault+'index.html'] = 1
        sitemap[self.pathdefault+'home.html'] = 0
        sitemap[self.pathdefault] = 2
        
        ### end ###
        
        lokasi = os.path.dirname(os.path.abspath(__file__))
        print lokasi
        
        '''
        #versi 3
        # jika file ada dan boleh diakses
        if (sitemap.get(self.pathdefault) == 0) #syntax masih salah
            file = open(self.path,"r")
            #print "file found"
            
            self.sendHeader()
            #print "header sent"
            
            self.sendFile()
            #print "file sent"
            
        # jika file uda dihapus
        if (sitemap.get(self.path) == 1) #syntax masih salah
            print self.path + "301 Moved Permanently"
            self.client.send("301 Moved Permanently\n")
            return 301
            
        # jika file tidak boleh diakses
        if (sitemap.get(self.path) == 2) #syntax masih salah
            print self.path + "403 Forbidden"
            self.client.send("403 Forbidden\n")
            return 403
            
        
        print self.path + "error 404 Not Found"
        self.client.send("404 Not Found\n")
        return 404
        
        '''
        #'''
        
        #versi 2
        lokasi = os.path.dirname(os.path.abspath(__file__))
        print lokasi
        try:
            file = open(self.path,"r")
            #print "file found"
            
            self.sendHeader()
            #print "header sent"
            
            self.sendFile()
            #print "file sent"
            
            if (self.path == "/home/ubuntu/workspace/halamanWeb/forbidden.html"):
                self.client.send("HTTP/1.1 403 Forbidden\nContent-Type: text/html;\r\n\r\n")
        except IOError:
            print self.path + "error 404 Not Found"
            self.client.send("404 Not Found\n")
        #'''
        '''
        # versi 1
        # dari iyus
        if (ekstensi == "html"):
            print "extensi == html" #debugging, monggo hapus
            lokasi = os.path.dirname(os.path.abspath(__file__))
            #print self.path
            try:
                #file = open(self.path,"r")
                now = datetime.datetime.now() #tanggal sekarang
                detilnow = now.strftime("%a, %d %b %Y %H:%M:%S")
                versipython= '.'.join(str(i) for i in sys.version_info)
                print versipython
                self.client.send("HTTP/1.1 200 OK\r\n") #jek ngawur versi httpnya
                self.client.send("Date : " + detilnow + " GMT\r\n")
                self.client.send("Server: " + versipython + "\r\n") #btw server bukannya apache ya?
                #print ukuran
            except IOError:
                self.client.send("404 not found\n")
                #self.send_error(404,'File Not Found: %s' % self.path)
        '''
            
    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            print 'recv: ', self.address, data # buat debugging
            # Ngoding dari sini
            
            # parsing
            if data:
                requestHeader = data.split(" ")[0]
                reqfile = data.split("/")[1].split("\n")[0]
                #reqfile = data.split(" ")[1].split("\n")[0]
                #elif requestHeader == GET:
                if (requestHeader == 'get'):
                    self.path = self.path + reqfile
                    print self.path
                    self.do_GET_HEAD()
                    #self.client.send(data)
            #elif requestHeader == HEAD:
                
            #elif requestHeader == POST:
            
            # Ngoding sampai sini
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    s = Server()
    s.run()
