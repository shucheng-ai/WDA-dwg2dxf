#!/usr/bin/env python3
import requests


url = 'http://localhost:8001/dwg2dxf/'
files = {'file': open('test.dwg', 'rb')}


r = requests.post(url, files=files)

with open('test.dxf', 'wb') as f:
    f.write(r.content)
    pass
