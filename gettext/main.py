import json
import base64
import os
import urllib.request
import http.client

gVisionUrl = 'https://vision.googleapis.com/v1/images:annotate?key='
GoogleApiKey = os.environ.get("GoogleApiKey")

def handler(event, context):
    # print("event")
    # print(event)

    if('file' in event):
        fileUrl = event['file']

        #download file locally
        request = urllib.request.Request(fileUrl)
        with urllib.request.urlopen(request) as response:
            encodedFile = base64.b64encode(response.read())
            b64 = encodedFile.decode()
    else:
        b64 = event['base64']
    print("image size "+str(len(b64)))

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
    header={'Content-Type': 'application/json'}
    req = urllib.request.Request(
            gVisionUrl + GoogleApiKey,
            data=json.dumps(payload).encode("utf-8"),
            headers=header,
            method='POST')
    req.add_header('ContentType','application/json')
    response = urllib.request.urlopen(req)
    responsejson = response.read().decode("utf-8")
    tmpvalue = json.loads(responsejson)
    if 'error' in tmpvalue["responses"][0]:
        print(tmpvalue)
        return {"textvalue":""}
    else:
        textvalue=tmpvalue["responses"][0]["fullTextAnnotation"]["text"]
        return {"textvalue":textvalue}
