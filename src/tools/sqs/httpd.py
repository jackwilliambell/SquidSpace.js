import http.server

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        # Turn off caching. Force reload everytime for testing purposes.
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

def run(server_class=http.server.HTTPServer, handler_class=MyHTTPRequestHandler):
    # We can't do port 80 because you have to be root. Need to make sure this 
    # is same as production or otherwise make sure the port in the URL matches
    # test or production.
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    # TODO: Write own interruptable serve forever loop to stop without control-c.
    print("Starting test server at http://localhost:8080/ – Press control-C to stop.")

