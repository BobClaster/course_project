#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("", 8080)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()
