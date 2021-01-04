from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
import cgi
class User():
    def __init__(self, idx, name, passwd, friends):
        self.id = idx
        self.name = name
        self.passwd = passwd
        self.friends = friends

# users = [User(1, "ilabo1", hashlib.sha256("ilabo213").hexdigest(), [2]), 
#     User(2, "ilabo2", hashlib.sha256("ilabo213").hexdigest(), [1])]        
users = [User(1, "ilabo1", "ilabo213", [2]), 
    User(2, "ilabo2", "ilabo213", [1])]        
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open("log.txt", "w") as f:
            #f.writelines(self.command+"")
            #f.writelines(self.headers+"")
            f.writelines(self.path+"")

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Hello World!", "utf-8"))

    def do_POST(self):
        with open("log.txt", "w") as f:
            f.writelines("header: "+self.headers.get('content-type'))

        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        if len(postvars) != 0:
            if self.path.startswith("/login"):
                for user in users:
                    if user.name == postvars[b"name"][0].decode("utf-8") and user.passwd == postvars[b"passwd"][0].decode("utf-8"):
                        self.send_response(200)
                        self.send_header("Content-type", "text/plain")
                        self.end_headers()
                        self.wfile.write(bytes("OK!", "utf-8"))
                        return
            
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Unknown request!", "utf-8"))

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def serve_on_port(port):
    server = ThreadingHTTPServer(("0.0.0.0",port), Handler)
    server.serve_forever()

# Thread(target=serve_on_port, args=[1111]).start()
serve_on_port(22222)