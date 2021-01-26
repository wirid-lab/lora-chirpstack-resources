import paho.mqtt.client as mqtt
import json
import base64
import requests

#Please Complete te next information for API connection
TOKEN_API_WIRIDLAB='<YOUR_AUTHENTICATION_WIRIDLAB_TOKEN>'
NODE_NAME_WIRIDLAB= '<NODE_NAME_WIRIDLAB_PLATFORM>'

#Please complete the next information for MQTT connection
SERVER_CHIRPSTACK='<IP_CHIRPSTACK_SERVER>'
MQTT_CHIRPSTACK_PORT= '<MQTT_CHIRPSTACK_CONNECTION_PORT>'
APPLICATION_ID='<APPLICATION_ID_CHIRPSTACK>'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("application/"+APPLICATION_ID+"/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #print('Mensaje --> Topic: {} \n'.format(msg.topic))
    print(str(msg.payload))
    x=str(msg.payload)
    y = json.loads(x)
    print(str(y))
    gateways = y['rxInfo']
    node = y['txInfo']
    fields = json.loads(y['objectJSON']) 
    print(str(fields))
    altit = fields.get('altitude', 'NA')
    barom = fields.get('barometer', 'NA')#['barometer']
    batte = fields.get('battery', 'NA')#['battery']
    gasre = fields.get('gasResistance', 'NA')#['gasResistance']
    humid = fields.get('humidity', 'NA')#['humidity']
    latit = fields.get('latitude', 'NA')#['latitude']
    longi = fields.get('longitude', 'NA')#['longitude']
    tempe = fields.get('temperature', 'NA')#['temperature']
    acelx = fields.get('acceleration_x', 'NA')#['acceleration_x']
    acely = fields.get('acceleration_y', 'NA')#['acceleration_y']
    acelz = fields.get('acceleration_z', 'NA')#['acceleration_z']
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

    #appid = y['applicationID']
    #appname = y['applicationName']
    #devname = y['deviceName']
    
    print("Enviando datos a la API.....")
    jsonData = [{}]
    jsonData[0]["altitude_s"] = altit
    jsonData[0]["barometer_s"] = barom
    jsonData[0]["battery_s"] = batte
    jsonData[0]["gasResistance_s"] = gasre
    jsonData[0]["humidity_s"] = humid
    jsonData[0]["latitude_s"] = latit
    jsonData[0]["longitude_s"] = longi
    jsonData[0]["temperature_s"] = tempe
    jsonData[0]["acceleration_x_s"] = acelx
    jsonData[0]["acceleration_y_s"] = acely
    jsonData[0]["acceleration_z_s"] = acelz
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

    #jsonData[0]["appID"] = appid
    #jsonData[0]["appName"] = appname
    #jsonData[0]["devName"] = devname
    #jsonData[0]["dataNode"] = datad
    #jsonData[0]["infNode"] = node
    #jsonData[0]["infGate"] = gateways
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
