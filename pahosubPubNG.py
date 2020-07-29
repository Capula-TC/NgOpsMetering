import random
import datetime
import time
import logging
import paho.mqtt.client as mqtt

import json
import argparse

parser = argparse.ArgumentParser(description="Send and receive messages through and MQTT connection.")
parser.add_argument('--endpoint', default="172.17.113.113", help="Your AWS IoT custom endpoint, not including a port. " +
                                                      "Ex: \"abcd123456wxyz-ats.iot.us-east-1.amazonaws.com\"")
parser.add_argument('--cert', help="File path to your client certificate, in PEM format.")
parser.add_argument('--key', help="File path to your private key, in PEM format.")
parser.add_argument('--root-ca', help="File path to root certificate authority, in PEM format. " +
                                      "Necessary if MQTT server uses a certificate that's not already in " +
                                      "your trust store.")
parser.add_argument('--client-id', default='samples-client-id', help="Client ID for MQTT connection.")
parser.add_argument('--topic', default="capula/asset001", help="Topic to subscribe to, and publish messages to.")
parser.add_argument('--range-start', default=0, type=int, help="Address range start at 0")
parser.add_argument('--range-end', default=9, type=int, help="Address range end. example 9")
parser.add_argument('--message', default="Hello World!", help="Message to publish. " +
                                                              "Specify empty string to publish nothing.")
parser.add_argument('--count', default=3, type=int, help="Number of messages to publish/receive before exiting. " +
                                                          "Specify 0 to run forever.")
parser.add_argument('--use-websocket', default=False, action='store_true',
    help="To use a websocket instead of raw mqtt. If you " +
    "specify this option you must specify a region for signing, you can also enable proxy mode.")
parser.add_argument('--signing-region', default='us-east-1', help="If you specify --use-web-socket, this " +
    "is the region that will be used for computing the Sigv4 signature")
parser.add_argument('--proxy-host', help="Hostname for proxy to connect to. Note: if you use this feature, " +
    "you will likely need to set --root-ca to the ca for your proxy.")
parser.add_argument('--proxy-port', type=int, default=8080, help="Port for proxy to connect to.")
#parser.add_argument('--verbosity', choices=[x.name for x in io.LogLevel], default=io.LogLevel.NoLogs.name,
#    help='Logging level')

# Using globals to simplify sample code
args = parser.parse_args()



#message builder
def getJsonMqttMessage():
    '''
        Loops through tag addresses to get property values then appends to a JSON object in the National Grid format.
    '''
    jsonMqttMessage = []

    paramaterDictionary = {
        1000:"active-power",
        1001:"reactive-power",
        1002:"voltage",
        1800:"breaker-setting",
        1801:"tap-position",
        1003:"power-available",
        1004:"wind-speed",
        1005:"wind-direction",
        1006:"ambient-temperature",
        1007:"global-radiation",
        1008:"state-of-charge",
        1009:"max-power-avail",
        1010:"min-power-avail"
    }

    for i in range (args.range_start,args.range_end):
        #gen.SetDataValuesLocal("eGeneric_Genesys/GGIO1.MX.AnIn00"+str(i)+".mag.f", type61850.FLOAT32(random.random()))
        genesysTagValue = random.random() #gen.GetDataValuesLocal("eGeneric_Genesys/GGIO1.MX.AnIn00"+str(i)+".mag.f")
        genesysTagTime = random.random() #gen.GetDataValuesLocal("eGeneric_Genesys/GGIO1.MX.AnIn00"+str(i)+".t")
        genesysTagQuality = random.random() #gen.GetDataValuesLocal("eGeneric_Genesys/GGIO1.MX.AnIn00"+str(i)+".q")
        
        jsonTagObject = {
            "parameter": str(paramaterDictionary[1000+i]),
            "value": str(genesysTagValue),
            "timestamp": str(genesysTagTime),
            "quality": str(genesysTagQuality)
        }
        jsonMqttMessage.append(jsonTagObject)
        
    return jsonMqttMessage

def on_message(client, userdata, message):
    topic=message.topic
    topicArray = topic.split("/")
    global deviceID
    deviceID = topicArray[1]
    global variableID
    variableID = topicArray[2]
    jsonPayload = str(message.payload.decode("utf-8"))
    print(jsonPayload)
    jsonMQTT = json.loads(jsonPayload)
    global valueMQTT
    valueMQTT = jsonMQTT["value"]
    global timestampMQTT
    timestampMQTT = jsonMQTT["timestamp"]
    print(mqttToOpcSubscribe(deviceID,variableID,valueMQTT,timestampMQTT))
    

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection retuerned code=", rc)


def on_log(client, userdata, level, buf):
    print("log: "+buf)

mqttClient = mqtt.Client(args.client_id)

def connect(host_address,myport):
    

    mqttClient.on_connect = on_connect
    mqttClient.on_log = on_log
    mqttClient.on_message = on_message

    print("connecting to broker")
    mqttClient.connect(host=host_address,port=myport)


#mqttClient.loop_start()
#mqttClient.subscribe("#")

if __name__ == '__main__':
    print("Connecting to {} with client ID '{}'...".format(
        args.endpoint, args.client_id))
    connect(args.endpoint,1883)
    print("Connected!")
    duration = 5
    print("Simulating values every "+ str(duration) +" seconds")
    
    publish_count = 1
    while (publish_count <= args.count) or (args.count == 0):
        mqttClient.publish(args.topic, str(getJsonMqttMessage()))
        time.sleep(int(duration))
        publish_count = publish_count - 1
    #mqttClient.loop_stop()