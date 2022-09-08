#!/usr/bin/env python3
from datetime import datetime
import urllib.parse
import http.server
import socketserver
import webbrowser
import threading
import writeSR

def weiter(values):
    values['PatientID'] = "000-000-002"
    values['PatientName'] = "Adam"
    values['PatientSex'] = "M"
    values['StudyDescription'] = "Visible Human Male"
    values['SeriesDescription'] = "Hip"
    values['InstanceCreationDate'] = "20050726"
    values['InstanceCreationTime'] = "102049"
    values['Date'] = datetime.now().strftime('%Y-%m-%d')
    values['Time'] = datetime.now().strftime('%H:%M:%S')

    for k, v in values.items():
        print(f"{k}: {v}")
    writeSR.writeSR(values)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = 'Hüftendoprothetik.html'
        print(self)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        datalength = int(self.headers['Content-Length'])
        field_data = self.rfile.read(datalength)
        fields = urllib.parse.parse_qs(field_data.decode('latin-1'), keep_blank_values=True)
        del fields['fulltext']
        values = {}
        for k, v in fields.items():
            values[k] = v[0] if v[0]!='' else '-'
        print(values)
        weiter(values)
        self.path = 'output.html'
        httpd.shutdown()
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


handler = MyHttpRequestHandler
addr = ("", 8000)
httpd = socketserver.ThreadingTCPServer(addr, handler)
webbrowser.open('http://127.0.0.1:8000', new=2, autoraise=True)
httpd.serve_forever()
httpd.server_close()

print("hi2")
