import hashlib
import requests
import simplejson
import os
import sys
    
from flask import Flask, request, Response

if len(sys.argv) > 1:
    SITE = sys.argv[1]
else:
    SITE = "https://github.com/"
EXCLUDED_HEADERS = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']

app = Flask(__name__)

METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
@app.route('/', defaults={'path': ''}, methods=METHODS)
@app.route('/<path:path>', methods=METHODS)
def catch_all(path):
    request_dict = {
        "method": request.method,
        "url": request.url.replace(request.host_url, SITE),
        "headers": {key: value for (key, value) in request.headers if key != 'Host'},
        "data": request.get_data(),
        "cookies": request.cookies,
        "allow_redirects": False
    }
    request_json = simplejson.dumps(request_dict, sort_keys=True)
    sha1 = hashlib.sha1(request_json.encode("utf-8")).hexdigest()
    path_req = os.path.join("cache", sha1 + ".req")
    path_resp = os.path.join("cache", sha1 + ".resp")
    if os.path.exists(path_req):
        print("Exists")
        with open(path_req, "r") as req:
            req_read = req.read()
            if req_read == request_json:
                with open(path_resp, "r") as dump:
                    response = simplejson.load(dump)
                    return Response(response["content"], response["status_code"], response["headers"])
        
    resp = requests.request(**request_dict)
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in EXCLUDED_HEADERS]
    response = {
        "content": resp.content,
        "status_code": resp.status_code,
        "headers": headers
    }
    response_json = simplejson.dumps(response, sort_keys=True)
    with open(path_resp, "w") as dump:
        dump.write(response_json)
    with open(path_req, "w") as req:
        req.write(request_json)
    return Response(response["content"], response["status_code"], response["headers"])
        

if __name__ == '__main__':
    app.run(debug=True)