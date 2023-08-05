import os
import json
from typing import Any, Callable, Dict, List
from base64 import b64decode
from hashlib import md5
from uuid import uuid4
from time import time
from functools import reduce
from .myhttp.http_classes import HttpRequest, HttpResponse, Session, decode_querystring, map_dictionary
from .pypress_classes import Application



##Midlewares de nivel global
'''
Configura el soporte para sesiones. Recibe una instancia global de Session.
'''
def session(s:Session):
    def inner(app: Application, req: HttpRequest, res: HttpResponse, next):
        app.session = s.create_session(req, res)
        next()
    return inner

contentTypes = {
    "text/": ["html", "css"],
    "text/javascript": ["js"],
    "text/html": ["htm"],
    "application/": ["json", "xml", "pdf"],
    "image/": ["gif", "png", "jpeg", "bmp", "webp"],
    "image/jpeg": ["jpg"],
    "audio/": ["mpeg", "webm", "ogg", "midi", "wav"],
    "text/plain": ["txt", "*"]
}

'''
Configura el soporte para archivos estáticos. "folder" se refiere a la ruta donde se buscarán los 
archivos estáticos.
'''
def static_files(folder: str):
    def result(app: Application, req: HttpRequest, res: HttpResponse, next):
        fileToSearch = os.sep.join([folder, req.path.replace('\\', '/')])
        #if 'scr' in req.path:
            #print(req.headers)
        if os.path.isfile(fileToSearch):
            extension = fileToSearch.split(".")[-1:][0]
            contentType = 'text/plain'
            for i in contentTypes:
                if extension in contentTypes[i]:
                    contentType = i
                    if contentType.endswith("/"):
                        contentType += extension
                    break
            #print(contentType)
            res.readFile(fileToSearch, contentType)
        else:
            next()
    return result

'''
Configura el control de acceso. Decodifica los parametros de autorización de la consulta.
Soporta "Bearer Token" y "Basic Authentication".
'''
def authorization(app:Application, req:HttpRequest, res:HttpResponse, next):
    authKey = 'Authorization'
    if authKey in req.headers:
        authType, authValue = req.headers[authKey].split(' ')
        req.authorization[authType] = ''
        if authType == 'Bearer':
            req.authorization[authType] = authValue
        elif authType == 'Basic':
            user, password = b64decode(authValue.encode()).decode().split(':')
            req.authorization[authType] = {'user':user, 'password':password}
        del req.headers[authKey]
        res.write(authValue)
    next()

'''
Configura el soporte para solicitudes del tipo "x-www-form-urlencoded". Carga los parametros de la
solitud enviados de esta manera en la propiedad "params" del objeto req.
'''
def body_parser(app:Application, req:HttpRequest, res:HttpResponse, next):
    if req.contentType != None and 'x-www-form-urlencoded' in req.contentType:
        params = map_dictionary(decode_querystring(req.body.strip()), '&', '=')
        for p in params:
            req.params[p] = params[p]
    next()


'''
Configura el soporte para solicitudes del tipo "multipart/form-data". Carga los parametros de la
solitud enviados de esta manera en la propiedad "params" del objeto req. Adicionalmente, en caso de 
existir archivos subidos en la solicitud, los guarda en la carpeta [tempFilesFolder] de manera temporal,
estableciendo la propiedad [files] del objeto req. Los archivos estarán disponibles durante la cantidad
de segundos definidos por el parametro [filesDuration]
''' 
def multipart_form_data_parser(tempFilesFolder, filesDuration=60):
    uploadedFiles = {}
    def inner_function(app:Application, req:HttpRequest, res:HttpResponse, next):
        if req.contentType != None and 'multipart/form-data' in req.contentType:
            contentType, boundary = [i.strip() for i in req.contentType.split(';')]
            req.contentType = contentType
            boundary = boundary.strip().replace('boundary=','')
            boundary = f'--{boundary}'
            #print(boundary)
            bodyParameters = [i.strip() for i in req.body.strip().split(boundary) if len(i.strip()) != 0 and i != '--']
            for param in bodyParameters:
                paramHeader, paramValue = param.split('\n\n', maxsplit=2)
                paramHeader = paramHeader.replace('\n', '; ').replace(': ', '=').replace('"', '')
                paramHeader = dict([tuple(i.split('=', maxsplit=2)) for i in paramHeader.split('; ')])
                if 'name' in paramHeader and len(paramHeader['name']) > 0:
                    req.params[paramHeader['name']] = paramValue
                elif 'filename' in paramHeader:
                    fileName = paramHeader['filename']
                    tempFilePath = os.sep.join([tempFilesFolder, str(uuid4()).replace('-', '')])
                    try:
                        with open(tempFilePath, 'w') as file:
                            file.write(paramValue)
                            req.files[fileName] = {'tempFilePath':tempFilePath}
                        uploadedFiles[tempFilePath] = time() + filesDuration
                        for file in uploadedFiles:
                            if uploadedFiles[file] < time():
                                os.remove(file)
                    except Exception as e:
                        print(str(e))
        next()
    return inner_function

'''Configura el soporte para solicitudes del tipo "json". En caso de existir un parametro json en el cuerpo
de la solicitud, establece la propiedad [data] del objeto req con dicho valor.'''
def json_body_parser(app:Application, req:HttpRequest, res:HttpResponse, next):
    if req.contentType in ['application/json', 'text/json']:
        try:
            req.data = json.loads(req.body.strip())
        except:
            res.status(400).write("Can't decode json body")
    next()

'''Configura la cabecera de control de acceso cors'''
def cors(app: Application, req: HttpRequest, res: HttpResponse, next):
    res.headers['Access-Control-Allow-Origin'] = "*"
    next()

'''Establece cabeceras por defecto en todas las respuestas. La cabeceras son determinadas bajo demanda
por el diccionario devuelto por la funcion [headersProvider]'''
def default_headers(headersProvider: Callable[[],Dict]):
    def child1(app: Application, req: HttpRequest, res: HttpResponse, next):
        headers = headersProvider()
        for h in headers:
            res.headers[h] = headers[h]
        next()
    return child1

since = time()
requestNumber = 0
'''Provee una función estandar para construir las cabeceras'''
def build_default_headers(baseHeaders: Dict[str, Any] = None):
    def inner():
        global requestNumber
        requestNumber += 1
        headers = baseHeaders or {}
        headers["Server-Epoch-Time"] = str(time())
        headers["Powered-By"] = "Python threadSnake beta"
        headers["Active-Since"] = since
        headers["Request-Count"] = requestNumber
        return headers
    return inner

'''Identifica al cliente imprimiendolo por la consola'''
def identify_client(app: Application, req: HttpRequest, res:HttpResponse, next):
    print(f'connection from {req.clientAddress}')
    next()

'''Ejecuta una accion determinada [action] siempre que se identifique la cabecera [headerName]'''
def header_inspector(headerName: str, action: Callable):
    def result(app: Application, req: HttpRequest, res: HttpResponse, next):
        if headerName in req.headers:
            action(req.headers[headerName])
        next()
    return result

'''
Generaliza la evaluacion de solicitudes, usando una funcion [predicate] que recibe un objeto req.
En caso de no cumplirse el [predicate] retorna al cliente una respuesta "400 Bad Request". En caso
de cumplirse el [predicate] continua la ejecucion normal.
'''
def validates_request(predicate:Callable[[HttpRequest], bool], onFailMessage:str = None, onFailStatus:int = 400):
    def child1(middleware:Callable):
        def child2(app:Application, req:HttpRequest, res: HttpResponse):
            if predicate(req):
                middleware(app, req, res)
            else:
                res.end(onFailMessage or "Bad Request", onFailStatus)
        return child2
    return child1

'''Especializacion de "request_validator" que evalua el content type de la solicitud.'''
def accepts(contentTypes:List[str]):
    def child1(middleware:Callable[[Application, HttpRequest, HttpResponse],None]):
        return validates_request(lambda r: r.contentType in contentTypes, onFailStatus=415)(middleware)
    return child1

'''Especializacion de "accepts" que espera un content type de Json.'''
def requires_json(middleware:Callable[[Application, HttpRequest, HttpResponse],None]):
    return accepts(['application/json', 'text/json'])(middleware)
    #return validates_request(lambda r: r.contentType in ['application/json', 'text/json'])(middleware)



'''Mide el tiempo que transcurre desde la llamada de este middleware hasta el final de la pila de ejecucion.
Idealmente mide el tiempo aproximado que tardó el servidor en servir la solicitud.'''
def time_measure(app:Application, req:HttpRequest, res:HttpResponse, next):
    startTime = time()
    next()
    interval = (time() - startTime) * 1000
    res.headers['process-time-ms'] = str(interval)
    #print(f"Request from {req.clientAddress} processed in {interval} milliseconds")


def validates_header(headerName:str, callback:Callable, notSuchHeaderStatus = 400):
    def child1(middleware):
        def child2(app:Application, req:HttpRequest, res:HttpResponse):
            if headerName in req.headers and callback(req.headers[headerName]):
                middleware(app, req, res)
            else:
                res.end(f"Missing or Invalid header value: {headerName}", notSuchHeaderStatus)
        return child2
    return child1


def requires_parameters(params):
    def inner(funct):
        def mutated(self:Application, req:HttpRequest, res:HttpResponse):
            missingParameters = [i for i in params if i not in [p for p in req.params]]
            if len(missingParameters) > 0:
                res.end('Missing parameters: ' + reduce(lambda a, b: f"{a}, {b}", missingParameters), 400)
            else:
                funct(self, req, res)
        return mutated
    return inner


def logs_execution(middleware):
    def inner(app:Application, req:HttpRequest, res:HttpResponse):
        print(f':::{req.method} {req.url} -> {middleware.__qualname__}')
        middleware(app, req, res)
    return inner


cache = {}
def uses_cache(cacheSize):
    def decorator(middleware):
        def inner(app:Application, req:HttpRequest, res:HttpResponse):
            if 'Cache-Control' in req.headers and req.headers['Cache-Control'] == 'no-cache':
                middleware(app, req, res)
                return
            reqHash = md5(req.raw.encode()).hexdigest()
            if reqHash in cache:
                res.cache(cache[reqHash])
            else:
                middleware(app, req, res)
                while len(cache) > cacheSize and cacheSize > 0:
                    del cache[list(cache.keys())[0]]
                cache[reqHash] = str(res)
        return inner
    return decorator