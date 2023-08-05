from functools import reduce
import json
from sys import path
from types import FunctionType
from typing import Callable, Dict, List
from .myhttp import Server, HttpRequest, HttpResponse, Session, RequestSession
from base64 import b64decode
from uuid import uuid4
import os
import re
import time
from importlib import __import__ as importpy

def routes_to(name):
    return __import__(name).R

class Router:
    def __init__(self):
        #print('router created')
        self.routes = {}

    def register_function(self, httpMethod, route):
        ref = self
        def inner(function):
            if httpMethod.upper() not in ref.routes:
            #if httpMethod.upper() not in Application.baseRoutes:
                ref.routes[httpMethod.upper()] = {route: function}
                #Application.baseRoutes[httpMethod.upper()] = {route: function}
            else:
                ref.routes[httpMethod.upper()][route] = function
                #Application.baseRoutes[httpMethod.upper()][route] = function
            return function
        return inner

    def get(self, route):
        return self.register_function('GET', route)

    def post(self, route):
        return self.register_function('POST', route)

    def configure(self, handler):
        self.stack.append(handler)
        return self

    def use_router(self, router, root):
        for method in router.routes:
            for action in router.routes[method]:
                if method not in self.routes:
                    self.routes[method] = {}
                self.routes[method][f'{root}{action}'] = router.routes[method][action]
        return self
        

    def __getattr__(self, method):
        def inner(route):
            return self.register_function(method.upper(), route)
        return inner


class Application(Server, Router):

    def __init__(self, port, connectionTimeout=None):
        Server.__init__(self, port, connectionTimeout)
        Router.__init__(self)
        self.stack = []
        self.session = {}

    def cli_loop(self, main_event: Callable):
        self.start()
        continueLoop = True
        while(continueLoop):
            try:
                continueLoop = main_event()
            except KeyboardInterrupt as e:
                print('[CLI EXIT]')
                break
            finally:
                self.stop()

    def onReceive(self, clientPort, data, clientAddress):
        if(len(data) == 0): return
        req = None
        res = HttpResponse()
        try:
            req = HttpRequest(data, clientAddress)
        except Exception as e:
            print(e)
            print(data)
            res.status(403, "BadRequest")
            clientPort.send(str(res).encode())
            return

        stack = self.stack.copy()

        def next():
            if len(stack) > 0 and not res.ended:
                stack.pop()(self, req, res, next)
        
        if ':' in req.path:
            pathParts = req.path.split('/')
            newPath = []
            for i in pathParts:
                queryPassParam = i.split(':')
                if len(queryPassParam) == 2:
                    req.params[queryPassParam[0]] = queryPassParam[1]
                else:
                    newPath.append(i)
            req.path = '/'.join(newPath)

        if req.method in self.routes:
            regularPaths = [i for i in self.routes[req.method]]
            for route in regularPaths:
                pattern = re.sub(r":([\w]+)", r"(?P<\1>[\\w]+)", route)
                pattern = "^" + pattern + "$"
                #print(f'{pattern} vs {req.path}')
                match = re.match(pattern, req.path)
                if match:
                    handler = self.routes[req.method][route]
                    queryParams = match.groupdict()
                    for i in queryParams:
                        req.params[i] = queryParams[i]
                    def middleware(app, req, res, next):
                        res.status(200)
                        handler(app, req, res)
                        next()
                    stack.append(middleware)
                    break

        stack.reverse()
        next()
        clientPort.send(str(res).encode())


Middleware = Callable[[Application, HttpRequest, HttpResponse, Callable[[], None]], None]

def BuildApplication(port: int, middlewares: List[Middleware], routers: Dict[str, Router]):
    app = Application(port)
    for m in middlewares:
        app.configure(m)
    for r in routers:
        app.use_router(routers[r], r)
    return app