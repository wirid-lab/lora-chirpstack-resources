import paho.mqtt.client as mqtt
import json
import base64
import requests

#Please Complete te next information for API connection
TOKEN_API_WIRIDLAB='iot-C5HcSy-bZWKwGBgOIHjsNT900n81kFrr'
NODE_NAME_WIRIDLAB= 'SF7HELTEC'

#Please complete the next information for MQTT connection
SERVER_CHIRPSTACK='10.0.2.86'
MQTT_CHIRPSTACK_PORT= '1883'
APPLICATION_ID='2'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("application/"+APPLICATION_ID+"/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    x=str(msg.payload)
    y = json.loads(x)
    gateways = y['rxInfo']
    node = y['txInfo']
    appid = y['applicationID']
    appname = y['applicationName']
    devname = y['deviceName']
    data = y['data']
    d = base64.b64decode(data)
    # Decoding the bytes to string
    datad = d.decode("UTF-8")


    frequ = node['frequency']
    modul = node['modulation']
    bandw = node['loRaModulationInfo']['bandwidth']
    coder = node['loRaModulationInfo']['codeRate']
    sprea = node['loRaModulationInfo']['spreadingFactor']
    grssi = y['rxInfo'][0]['rssi']
    gsnr = y['rxInfo'][0]['loRaSNR']
    gchan = y['rxInfo'][0]['channel']
    grfch = y['rxInfo'][0]['rfChain']
    gcrc = y['rxInfo'][0]['crcStatus']



    print("Enviando datos a la API.....")
    jsonData = [{}]
    jsonData[0]["appID"] = appid
    jsonData[0]["appName"] = appname
    jsonData[0]["devName"] = devname
    jsonData[0]["dataNode"] = datad
    jsonData[0]["infNode"] = node
    jsonData[0]["infGate"] = gateways


    jsonData[0]['frequency_s'] = frequ
    jsonData[0]['modulation_s'] = modul
    jsonData[0]['bandwidth_s'] = bandw
    jsonData[0]['codeRate_s'] = coder
    jsonData[0]['spreadingFactor_s'] = sprea
    jsonData[0]['rssi_s'] = grssi
    jsonData[0]['loRaSNR_s'] = gsnr
    jsonData[0]['channel_s'] = gchan
    jsonData[0]['rfChain_s'] = grfch
    jsonData[0]['crcStatus_s'] = gcrc

    print (jsonData)

    jsonData = json.dumps(jsonData, indent=4)
    headers = {"WIRID-LAB-AUTH-TOKEN": TOKEN_API_WIRIDLAB, "Content-Type": "application/json"}
    info = requests.post("https://api.wiridlab.site/api/iot/devices/"+ NODE_NAME_WIRIDLAB.lower() , headers=headers, data=jsonData, timeout=None)
    dataAPI = info.json()

    if (info.status_code == 200):
        print ("  Request API")
        print(json.dumps(dataAPI, indent=4, sort_keys=True))
    else:
        print ("Error sending information")
        print(json.dumps(dataAPI, indent=4, sort_keys=True))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(SERVER_CHIRPSTACK, MQTT_CHIRPSTACK_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
