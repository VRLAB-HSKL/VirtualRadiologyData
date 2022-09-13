#!/usr/bin/env python3
from datetime import datetime
import urllib.parse
import http.server
import socketserver
import webbrowser
import threading
import writeSR
import re

def createSR(values):
    imgdata = {}
    imgdata['PatientID'] = "000-000-002"
    imgdata['PatientName'] = "Adam"
    imgdata['PatientSex'] = "M"
    imgdata['StudyDescription'] = "Visible Human Male"
    imgdata['SeriesDescription'] = "Hip"
    imgdata['InstanceCreationDate'] = "20050726"
    imgdata['InstanceCreationTime'] = "102049"
    imgdata['Date'] = datetime.now().strftime('%Y-%m-%d')
    imgdata['Time'] = datetime.now().strftime('%H:%M:%S')
    with open("huefttepV1templ.xml", 'r') as sr:
        txt = sr.read()
    for k, v in imgdata.items():
        pat = f"{{{k}}}"
        txt = re.sub(pat, v, txt)
    with open("output.xml", 'w') as out:
        out.write(txt)
    if __name__=="__main__":
        for k, v in values.items():
            print(f"{k}: {v}")
    writeSR.writeSR(values)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = 'Hüftendoprothetik.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        global httpd
        datalength = int(self.headers['Content-Length'])
        field_data = self.rfile.read(datalength)
        fields = urllib.parse.parse_qs(field_data.decode('latin-1'), keep_blank_values=True)
        del fields['fulltext']
        values = {}
        for k, v in fields.items():
            values[k] = v[0] if v[0]!='' else '-'
        createSR(values)
        self.path = 'output.html'
        httpd.shutdown()
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def main():
    global httpd
    handler = MyHttpRequestHandler
    addr = ("", 8000)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(addr, handler)
    webbrowser.open(f'http://127.0.0.1:{addr[1]}', new=2, autoraise=True)
    httpd.serve_forever()
    httpd.server_close()

if __name__ == "__main__":
    main()
