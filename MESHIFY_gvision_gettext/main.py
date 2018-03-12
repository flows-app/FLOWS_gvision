import boto3
import json
import base64
import urllib.request
import http.client

SSM = boto3.client('ssm')

gVisionUrl = 'https://vision.googleapis.com/v1/images:annotate?key='

def handler(event, context):
    print("event")
    print(event)

    fileUrl = event['file']

    response = SSM.get_parameter(
      Name='/MESHIFY/systems/google/apikey',
      WithDecryption=True
    )
    gVisionApiKey =response['Parameter']['Value']

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
    print(gVisionUrl + gVisionApiKey)
    header={'Content-Type': 'application/json'}
    req = urllib.request.Request(
            gVisionUrl + gVisionApiKey,
            data=json.dumps(payload).encode("utf-8"),
            headers=header,
            method='POST')
    req.add_header('ContentType','application/json')
    response = urllib.request.urlopen(req)
    print(response.read())

    return {"status":"done"}
