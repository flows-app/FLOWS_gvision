import json
import base64
import os
import urllib.request
import http.client

gVisionUrl = 'https://vision.googleapis.com/v1/images:annotate?key='
GoogleApiKey = os.environ.get("GoogleApiKey")

def handler(event, context):
    print("event")
    print(event)

    fileUrl = event['file']

    #download file locally
    request = urllib.request.Request(fileUrl)
    with urllib.request.urlopen(request) as response:
        encodedFile = base64.b64encode(response.read())
        b64 = encodedFile.decode()


    payload = {
        "requests": [{
            "image": {
                "content": b64
            },
            "features": [{
                "type": "DOCUMENT_TEXT_DETECTION"
            }]
        }]
    }
    print(gVisionUrl + GoogleApiKey)
    header={'Content-Type': 'application/json'}
    req = urllib.request.Request(
            gVisionUrl + GoogleApiKey,
            data=json.dumps(payload).encode("utf-8"),
            headers=header,
            method='POST')
    req.add_header('ContentType','application/json')
    response = urllib.request.urlopen(req)
    print(response.read())

    return {"status":"done"}
