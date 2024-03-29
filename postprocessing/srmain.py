import urllib.parse
import http.server
import socketserver
import webbrowser
if __name__ != "__main__":
    from postprocessing import writeSR, templconf

def createSR(values):
    if __name__=="__main__":
        for k, v in values.items():
            print(f"{k}: {v}")
    else:
        writeSR.writeSR(values)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        http.server.SimpleHTTPRequestHandler.end_headers(self)
        
    def send_my_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def do_GET(self):
        if self.path == '/':
            self.path = f'./template/{templconf.fname}/{templconf.fname}.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        datalength = int(self.headers['Content-Length'])
        field_data = self.rfile.read(datalength)
        fields = urllib.parse.parse_qs(field_data.decode('utf-8'), keep_blank_values=True)
        del fields['fulltext']
        values = {}
        for k, v in fields.items():
            values[k] = v[0] if v[0]!='' else '-'
        createSR(values)
        self.path = './output/output.html'
        templconf.httpd.shutdown()
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def main():
    handler = MyHttpRequestHandler
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    templconf.httpd = socketserver.ThreadingTCPServer((templconf.ip, templconf.port), handler)
    webbrowser.open(f'http://{templconf.ip}:{templconf.port}', new=0, autoraise=True)
    templconf.httpd.serve_forever()
    templconf.httpd.server_close()
    print("Server was shut down!")

if __name__ == "__main__":
    import templconf
    templconf.fname = 'CT-Thorax_Covid-19'
    main()
