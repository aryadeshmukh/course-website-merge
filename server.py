import http.server
import socketserver
# from database.database import Database

PORT = 8080
handler = http.server.CGIHTTPRequestHandler

with http.server.HTTPServer(("", PORT), handler) as httpd:
    # open('./course-links.txt', 'w').close()
    # db = Database()
    # db.clear()
    print("serving at port", PORT)
    httpd.serve_forever()