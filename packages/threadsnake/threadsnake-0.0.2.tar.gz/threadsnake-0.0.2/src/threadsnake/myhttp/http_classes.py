from functools import reduce
import json
from re import L
import re
import socket
from threading import Thread
import threading
import time
import uuid
import os
from enum import Enum, IntEnum

class RedirectType(IntEnum):
    MOVED_PERMANENT = 301
    PERMANENT_REDIRECT = 308
    FOUND = 302
    SEE_OTHER = 303
    TEMPORARY_REDIRECT = 307
    MULTIPLE_CHOICE = 301
    NOT_MODIFIED = 304

path = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'response_codes.txt'
responseCodes = {}
with open(path, 'r') as f:
    for l in [i.strip() for i in f.readlines()]:
        values = l.split('\t')
        if len(values) > 1:
            responseCodes[int(values[0])] = values[1]
        else:
            print(f'Invalid line on response_codes.txt: {values}')


def decode_querystring(data):
    data = data.replace('+', ' ').replace('%20', ' ')#space
    data = data.replace('%2B', '+')#space
    data = data.replace('%7E', '~')#space
    references = [(i, chr(int(re.findall(r'[\d]+', i)[0]))) for i in re.findall(r'&#[\d]+;', data)]
    for ref in references:
        data = data.replace(ref[0], ref[1])
    return data

def map_dictionary(data, rowSeparator, keySeparator):
    return dict([
        tuple([j.strip() for j in i.split(keySeparator, 1)])
        for i in data.split(rowSeparator) if len(i.split(keySeparator)) == 2
    ])

class HttpResponse:
    def __init__(self):
        self.resposeStatus = 404
        self.resposeText = 'NotFound'
        self.headers = {
            "Content-Type": "text/plain",
            "Content-Length": "0",
            "Connection": "close"
        }
        self.cookieHeaders = []
        self.body = ""
        self.ended = False
        self.contentDisposition = ''
        self.cacheValue = None

    def cache(self, cacheValue):
        self.cacheValue = cacheValue

    def end(self, data, status = None):
        self.ended = True
        self.status(status or 200)
        return self.write(data)

    def redirect(self, url, statusCode = None):
        self.status(statusCode or RedirectType.TEMPORARY_REDIRECT)
        self.headers = {"Location": url}
        self.body = ""
        return self

    def status(self, resposeStatus, resposeText=None):
        self.resposeStatus = resposeStatus
        if resposeText == None and resposeStatus in responseCodes:
            self.resposeText = responseCodes[resposeStatus]
        else:
            self.resposeText = resposeText or "OK"
        return self

    def content_type(self, value):
        self.headers["Content-Type"] = value
        return self

    def json(self, data):
        self.body = json.dumps(data)
        return self.content_type("text/json")

    def write(self, data):
        self.body += data
        return self

    def html(self, data):
        return self.content_type('text/html').write(str(data))

    def read_file(self, fileName, contentType=None):
        with open(fileName, 'r') as f:
            self.body += f.read()
        self.status(200)
        return self.content_type(contentType or "text/plain")

    def transmit_as_file(self, fileName, data, contentType=None):
        self.set_content_disposition('attachment', fileName)
        self.body = data
        self.status(200)
        return self.content_type(contentType or "text/plain")

    def set_content_disposition(self, contentDisposition, fileName = None):
        self.contentDisposition = contentDisposition
        if fileName is not None:
            self.contentDisposition += f'; fileName="{fileName}"'
        return self

    def download_file(self, path, fileName, contentType=None):
        self.set_content_disposition('attachment', fileName)
        return self.read_file(path, contentType)

    def __str__(self):
        if not self.cacheValue == None:
            return self.cacheValue
        result = f"HTTP/1.1 {self.resposeStatus} {self.resposeText}\n"
        if 'Location' not in self.headers: self.headers["Content-Length"] = len(self.body)
        if len(self.contentDisposition or '') > 0:
            self.headers['Content-Disposition'] = self.contentDisposition 
        mappedHeaders = [f"{i}:{self.headers[i]}\n" for i in self.headers]
        for cookie in self.cookieHeaders:
            print(cookie)
            mappedHeaders.append(f"Set-Cookie:{cookie}\n")
        result += reduce(lambda a, b: a + b, mappedHeaders)
        result += '\n'
        result += self.body
        return result

    def set_cookie(self, name, value, durationSec = None, domain = None, path = None):
        cookieString = value
        if durationSec != None: 
            expireUTC = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(time.time() + durationSec))
            cookieString += f"; Expires={expireUTC}"
        if domain != None: cookieString += f"; Domain={domain}"
        if path != None: cookieString += f"; Path={path}"
        self.cookieHeaders.append(f"{name}={cookieString}")

class HttpRequest:
    def __init__(self, raw, address):
        self.clientAddress = address
        self.load(raw)

    def load(self, raw):
        self.raw = raw
        self.authorization = {}
        self.files = {}
        headerAndBody = self.raw.split('\n\n', 1)
        self.headers = headerAndBody[0].split('\n')
        if len(headerAndBody) > 1:
            self.body = headerAndBody[1]
        else:
            self.body = ''
        firstLine = self.headers[:1][0].split(' ')
        self.headers = self.headers[1:]
        self.method = firstLine[0]
        self.httpVersion = firstLine[2] if len(firstLine) >= 2 else 'HTTP/1.1'
        self.url = firstLine[1] if len(firstLine) >= 1 else ''
        self.querystring = self.url.split('?', 1)[1] if '?' in self.url else ''
        self.querystring = decode_querystring(self.querystring)
        self.path = self.url.split('?')[:1][0]
        self.params = map_dictionary(self.querystring, '&', '=')
        self.data = {}

        #Soved with body_parser
        #if self.method == 'POST' and len(self.body) != 0:
        #    postParams = map_dictionary(self.body, '&', '=')
        #    for p in postParams:
        #        self.params[p] = postParams[p]
        
        self.headers = dict([
            tuple([j.strip() for j in i.split(':', 1)]) for i in self.headers
            if len(i.split(':')) == 2
        ])
        self.contentType = self.headers.get('Content-Type', None)
        self.cookies = {}
        if 'Cookie' in self.headers:
            self.cookies = dict([tuple([j.strip() for j in i.split('=')]) for i in self.headers['Cookie'].split(';') if len(i.split('=')) == 2])
        pass



class ServerWorker(Thread):
    def __init__(self, action):
        Thread.__init__(self)
        self.action = action
    
    def run(self):
        self.action()

class Server(Thread):
    def __init__(self, port=80, connectionTimeout=None):
        Thread.__init__(self)
        self.connectionTimeout = connectionTimeout or 0.1
        self.maxPacket = 32768
        self.port = port
        self.server_active = True

    def stop(self):
        if self.serverSocket != None:
            self.server_active = False
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            srv.connect(('localhost', self.port))
            srv.shutdown(socket.SHUT_RDWR)
            srv.close()
            self.serverSocket = None

    def __exit__(self):
        self.stop()

    def __del__(self):
        self.stop()

    def onConnect(self, clientPort, clientAddress):
        pass

    def onReceive(self, clientPort, data):
        raise NotImplementedError()

    def receive(self, clientPort):
        rdata = []
        timeout = clientPort.gettimeout()
        try:
            clientPort.settimeout(self.connectionTimeout)
            while True:
                try:    
                    rdata.append(clientPort.recv(self.maxPacket))
                except:
                    break
        finally:
            clientPort.settimeout(timeout)
        raw = ''.join([i.decode() for i in rdata])
        return ''.join([i + '\n' for i in raw.splitlines()])

    def next_free(self, port, max_port=65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('', port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError('no free ports')

    def run(self):
        self.port = self.next_free(self.port)
        print(f'listening on {self.port}...')
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        self.serverSocket.bind(('', self.port))
        self.serverSocket.listen(5)
        while self.server_active:
            try:
                #print('ON Accept')
                (clientSocket, address) = self.serverSocket.accept()
                if not self.server_active:
                    break
                #print('ACCEPT ENDED')
                def handler():
                    localSocketRef = clientSocket
                    self.onConnect(localSocketRef, address)
                    try:
                        raw_data = self.receive(localSocketRef)
                        self.onReceive(localSocketRef, raw_data, address)
                    except socket.timeout:
                        print('timeout')
                    except Exception as e:
                        print('Exception in handler')
                        print(e)
                        pass
                    finally:
                        try:
                            localSocketRef.close()
                        except:
                            print('Error closing the socket...')
                ServerWorker(handler).start()
            except OSError as o:
                print('There was an OSError!')
                self.stop()
                break
            except Exception as e:
                print('Exception in listen loop')
                print(e)
                self.stop()
                break
        #print('block ended!')

class Session:
    def __init__(self, cookieName = None):
        self.cookieName = cookieName or 'sessionId'
        self.sessions = {}

    def ensure_session(self, req:HttpRequest, res:HttpResponse):
        sessionId = ''
        if self.cookieName not in req.cookies:
            sessionId = str(uuid.uuid4())
            res.set_cookie(self.cookieName, sessionId)
            req.cookies[self.cookieName] = sessionId
        else:
            sessionId = req.cookies[self.cookieName]
        if sessionId not in self.sessions:
            self.sessions[sessionId] = {}
        return sessionId

    def get(self, req:HttpRequest, res:HttpResponse, key):
        sessionId = self.ensure_session(req, res)
        if key not in self.sessions[sessionId]:
            return None
        else:
            return self.sessions[sessionId][key]

    def set(self, req:HttpRequest, res:HttpResponse, key, value):
        sessionId = self.ensure_session(req, res)
        self.sessions[sessionId][key] = value

    def create_session(self, req:HttpRequest, res:HttpResponse):
        return RequestSession(req, res, self)

class RequestSession:
    def __init__(self, req:HttpRequest, res:HttpResponse, session:Session):
        self.req = req
        self.res = res
        self.session = session
    
    def __setitem__(self, key, value):
        self.session.set(self.req, self.res, key, value)

    def __getitem__(self, key):
        return self.session.get(self.req, self.res, key)
