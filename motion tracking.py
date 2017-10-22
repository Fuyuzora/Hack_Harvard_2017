####################################

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'b4945d3f-2af8-457d-8daa-95665ff9539e',
}

params = urllib.parse.urlencode({
    # Request parameters
    'sensitivityLevel': 'medium',
    'frameSamplingValue': '10',
    'detectionZones': 'detectionZones=0,0;0.5,0;1,0;1,0.5;1,1;0.5,1;0,1;0,0.5',
    'detectLightChange': 'False',
    'mergeTimeThreshold': '0.0',
})

body = {'url': "PUT A URL HERE"}

try:
    conn = http.client.HTTPSConnection('eastcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/video/v1.0/detectmotion?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################