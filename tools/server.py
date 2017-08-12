#!/usr/bin/python

import mimetypes
import os
import platform
import sys

if sys.version_info[0] > 2:
    from urllib.parse import urlparse
    from http.server import HTTPServer
    from http.server import BaseHTTPRequestHandler
else:
    from urlparse import urlparse
    from BaseHTTPServer import HTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def handler(self):
        pathname = urlparse(self.path).path
        location = root + pathname;
        status_code = 404
        headers = {}
        if os.path.exists(location) and os.path.isdir(location):
            if not location.endswith("/"):
                status_code = 302
                headers = { "Location": pathname + "/" }
            else:
                location += "index.html"
        buffer = None
        if os.path.exists(location) and not os.path.isdir(location):
            extension = os.path.splitext(location)[1]
            content_type = mimetypes.types_map[extension]
            if content_type:
                with open(location, "rb") as binary:
                    buffer = binary.read()
                status_code = 200
                headers = {
                    "Content-Type": content_type,
                    "Content-Length": len(buffer)
                }
        print(str(status_code) + " " + self.command + " " + self.path)
        self.send_response(status_code)
        for key in headers:
            self.send_header(key, headers[key])
        self.end_headers()
        if status_code == 200 and self.command != "HEAD":
            self.wfile.write(buffer)
    def do_GET(self):
        self.handler();
    def do_HEAD(self):
        self.handler();
    def log_message(self, format, *args):
        return

root = "."
port = 8080
browse = False
args = sys.argv[1:]
while len(args) > 0:
    arg = args.pop(0)
    if (arg == "--port" or arg == "-p") and len(args) > 0 and args[0].isdigit(): 
        port = int(args.pop(0))
    elif arg == "--browse" or arg == "-b":
        browse = True
    else:
        root = arg
server = HTTPServer(("localhost", port), HTTPRequestHandler)
url = "http://localhost:" + str(port)
print("Serving '" + root + "' at " + url + "...")
if browse:
    command = "xdg-open";
    if platform.system() == "Darwin":
        command = "open"
    elif platform.system() == "Windows":
        command = 'start ""'
    os.system(command + ' "' + url.replace('"', '\"') + '"')
server.serve_forever()