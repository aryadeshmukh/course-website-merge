import http.server
import socketserver

PORT = 8080
handler = http.server.CGIHTTPRequestHandler

with http.server.HTTPServer(("", PORT), handler) as httpd:
    open('../course-links.txt', 'w').close()
    print("serving at port", PORT)
    httpd.serve_forever()