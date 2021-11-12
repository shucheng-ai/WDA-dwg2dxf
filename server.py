#!/usr/bin/env python3
import os
import logging
import time
from datetime import datetime
import subprocess as sp
import json
from flask import Flask, request, jsonify, send_from_directory

LOG_LEVEL = 'INFO'
LOG_PATH = 'dwg2dxf.log'
LOG_DIR = 'log'
PORT=8001

try:
    from local_config import *
except:
    pass

fmt = "%(asctime)s | %(levelname)s | %(message)s | %(filename)s/%(funcName)s/%(lineno)d"
datefmt = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    # DEBUG,INFO,WARNING,ERROR,CRITICAL
    level=LOG_LEVEL,
    format=fmt,
    datefmt=datefmt,
    filename=LOG_PATH,
    filemode='w'
)

logger = logging.getLogger('dwg2dxf')
logger.warning("logger:")
logger.warning(f"logger level:{LOG_LEVEL}")
logger.warning(f"logger path:{LOG_PATH}")

# 最后每个请求有个序列号，格式为 p-c
# 其中p是一个unix时间，代表服务器启动的时间
# c是本次服务器启动后的请求数，从0开始
epoch = int(time.time())
serial_prefix = '%d-' % epoch
serial_count = 0

# 获得请求序列号
def get_serial ():
    global serial_prefix
    global serial_count
    s = serial_prefix + '%06d' % serial_count
    serial_count += 1
    return s

# 每个请求对应一个目录, 有一个日期的目录结构，最后目录名为序列号
# LOG_DIR/年月日/时/序列号
def make_request_dir (serial):
    now = datetime.now()
    now_date = now.date()
    now_time = now.time()
    path = '%s/%04d%02d%02d/%02d/%s' % (LOG_DIR, now_date.year, now_date.month, now_date.day, now_time.hour, serial)
    os.makedirs(path, exist_ok=True)
    return path

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index ():
    return "post dwg file to /dwg2dxf/"

def convert (input_fmt, output_fmt, input_fname, output_fname, attachment_fname_fn):
    upload = request.files['file']
    serial = get_serial()
    wdir = make_request_dir(serial)
    idir = os.path.join(wdir, 'input')
    odir = os.path.join(wdir, 'output')
    os.makedirs(idir, exist_ok=True)
    os.makedirs(odir, exist_ok=True)
    with open(os.path.join(wdir, 'meta.json'), 'w') as f:
        json.dump({
            'filename': upload.filename,
            'input_format': input_fmt,
            'output_format': output_fmt
        }, f)
        pass
    upload.save(os.path.join(idir, input_fname))
    cmd = 'xvfb-run /usr/bin/ODAFileConverter_21.3.0.0/ODAFileConverter %s %s ACAD2007 %s 0 1' % (idir, odir, output_fmt)
    sp.call(cmd, shell=True)
    attachment_fname = attachment_fname_fn(upload.filename)
    return send_from_directory(directory=odir, filename=output_fname, as_attachment=True, attachment_filename=attachment_fname)

def dxf_to_dwg (dxfpath, dwgpath):
    
    command = "xvfb-run /usr/bin/ODAFileConverter_21.3.0.0/ODAFileConverter " + dxfpath + " " + dwgpath +" ACAD2007 DWG 0 1"
    os.system(command)
    
    pass

def replace_ext (fname, ext):
    out = 'output'
    try:
        out = fname.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    except:
        pass
    return out + ext

@app.route('/dwg2dxf/', methods=['POST'])
def dwg2dxf ():
    return convert('DWG', 'DXF', 'upload.dwg', 'upload.dxf', lambda x: replace_ext(x, '.dxf'))

@app.route('/dxf2dwg/', methods=['POST'])
def dxf2dwg ():
    return convert('DXF', 'DWG', 'upload.dxf', 'upload.dwg', lambda x: replace_ext(x, '.dwg'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)
    pass


