"""## SquidSpace.js Serve Command

The SquidSpace.js 'serve' command creates a web server for static files in the 
current working directory using the address 'http://localhost:8000/'. The server
will run until you force it to quit by pressing 'ctrl-C'.

For more information on SquidSpace.js, please refer to the documentation 
located in the project repo at https://github.com/jackwilliambell/SquidSpace.js"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""

import signal
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

def interrupt_handle(signum,frame):
    print("\nctrl-C received. Quit!")
    quit()

def runServer(server_class=http.server.HTTPServer, handler_class=MyHTTPRequestHandler):
    # We can't do port 80 because you have to be root. Need to make sure this 
    # is same as production or otherwise make sure the port in the URL matches
    # test or production.
    print("Starting test server at http://localhost:8000/ – Press ctrl-C to stop.")
    signal.signal(signal.SIGINT,interrupt_handle)

    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    # TODO: Write own interruptable serve forever loop to stop without control-c.

