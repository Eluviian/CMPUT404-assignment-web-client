#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("a")
        self.socket.settimeout(1)
        self.socket.connect((host, port))
        #print("CONNECTION MADE")
        
        return None

    def get_code(self, data):
        data_list = data.split()
        #print("DATA*******************\n", data_list, "\n**************************")
        #print("DATA TYPE:", type(data_list))   #list
        return int(data_list[1])

    def get_headers(self,data):
        data = data.split("\n")
        end = data.index("\r")
        #print("END:",end)
        #print("DATA LIST:",data)

        return "\n".join(data[1:end])
        

    def get_body(self, data):
        data = data.split("\n")
        print("DATA LIST:",data)
        start = data.index("\r")
        print("START:",start)
        return data[start+1]

    def sendall(self, data):
        self.socket.sendall(data)
        #print("SENT DATA:", data, "\n***************************************\n")
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            print("E")
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):  #what to do with args?
        #print("in GET, url:", url)
        #print("args:", args)
        code = 500
        body = ""

        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname.encode('utf-8')
        port = parsed_url.port
        scheme = parsed_url.scheme
        path = parsed_url.path.encode('utf-8')

        if not path:
            path = b"/"

        if not port:
            if scheme == "http":
                port = 80
            if scheme == "https":
                port = 443
        
        request = b"GET "+path+b" "+b"HTTP/1.1\r\n"
        request += b"Host: "+hostname+b"\r\n"
        request += b"Accept-Charset: UTF-8\r\n"
        request += b"Connection:Close\r\n"
        request += b"\r\n"
        #print(request)
        print("HOSTNAME, PORT: ", hostname, port)
        self.connect(hostname,port)

        
        


        #handle if path is not "/", this should be default if nothing specified
        #set path outside of sendall()     ?
        self.sendall(request)

        #illegal request
        #print(self.recvall(self.socket)) #get code and body from this
        
        recvd = self.recvall(self.socket)
        code = self.get_code(recvd)
        headers = self.get_headers(recvd)
        body = self.get_body(recvd)

        print("*********************\nRECVD:\n", recvd, "\n***********************")

        print("CODE:",code)
        print("HEADERS:",headers)
        print("BODY:",body)

        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname.encode('utf-8')
        port = parsed_url.port
        scheme = parsed_url.scheme
        path = parsed_url.path.encode('utf-8')

        if not path:
            path = b"/"

        if not port:
            if scheme == "http":
                port = 80
            if scheme == "https":
                port = 443


        if args:
            args = urllib.parse.urlencode(args)
            args = args.encode('utf-8')
            arg_length = str(len(args)).encode('utf-8')
        else:
            arg_length = b"0"
        

        request = b"POST /04-HTTP.html HTTP/1.1\r\n"
        request += b"Host: "+hostname+b"\r\n"
        request +=b"Accept-Encoding: gzip\r\n"
        request += b"Content-Length: "+arg_length+b"\r\n"
        request += b"Connection: Close\r\n"
        request += b"DNT: 1\r\n"
        request += b"\r\n"

        if args:
            request += args

        
        self.connect(hostname,port)  

        print("REQUEST:",request.decode())
        self.sendall(request)

        #illegal request
        #print(self.recvall(self.socket)) #get code and body from this
        
        recvd = self.recvall(self.socket)
        code = self.get_code(recvd)
        headers = self.get_headers(recvd)
        body = self.get_body(recvd)

        print("*********************\nRECVD:\n", recvd, "\n***********************")

        print("CODE:",code)
        print("HEADERS:",headers)
        print("BODY:",body)


        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    #print(sys.argv)
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))


