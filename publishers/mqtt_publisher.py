# script simulates sensor data publishing (e.g., temperature, humidity) via MQTT using the certs received during provisioning.
#Example Commands
  1. Provision a New Device:
	python provisioning/provision_device.py --device-id temp-001

#This creates a new Thing temp-001, and stores:

#certs/temp-001-certificate.pem.crt

#certs/temp-001-private.pem.key

#Start Simulating Data:

#python publishers/mqtt_publisher.py \
#  --thing-name temp-001 \
#  --cert certs/temp-001-certificate.pem.crt \
#  --key certs/temp-001-private.pem.key

# This will publish JSON files like:

#{
#  "timestamp": 1695666545,
#  "temperature": 24.3,
#  "humidity": 58.2,
#  "vibration": 0.053
#}

#Prerequisites

#Ensure that:

#AWS IoT endpoint is set in both scripts (IOT_ENDPOINT)

#Root CA and claim certs exist in certs/

#Also, you have created a Fleet Provisioning Template and claim cert in AWS

#IAM role permissions are correctly set for fleet provisioning and MQTT publish




import json
import time
import random
import argparse
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# --- CONFIGURATION ---
IOT_ENDPOINT = "<your-iot-endpoint>.amazonaws.com"  # Same endpoint
ROOT_CA = "certs/AmazonRootCA1.pem"
# ----------------------

def create_mqtt_client(thing_name, cert_path, key_path):
    mqtt_client = AWSIoTMQTTClient(thing_name)
    mqtt_client.configureEndpoint(IOT_ENDPOINT, 8883)
    mqtt_client.configureCredentials(ROOT_CA, key_path, cert_path)
    mqtt_client.configureOfflinePublishQueueing(-1)
    mqtt_client.configureDrainingFrequency(2)
    mqtt_client.configureConnectDisconnectTimeout(10)
    mqtt_client.configureMQTTOperationTimeout(5)
    return mqtt_client

def simulate_publish(mqtt_client, topic, interval=5):
    while True:
        payload = {
            "timestamp": int(time.time()),
            "temperature": round(random.uniform(18.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 70.0), 2),
            "vibration": round(random.uniform(0.01, 0.2), 3)
        }
        print(f"📤 Publishing to {topic}: {payload}")
        mqtt_client.publish(topic, json.dumps(payload), 1)
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--thing-name", required=True, help="Registered thing name")
    parser.add_argument("--cert", required=True, help="Path to device cert PEM")
    parser.add_argument("--key", required=True, help="Path to private key PEM")
    parser.add_argument("--group", default="group1", help="Device group name")
    args = parser.parse_args()

    mqtt_client = create_mqtt_client(args.thing_name, args.cert, args.key)
    mqtt_client.connect()

    topic = f"iot/{args.group}/{args.thing_name}/data"
    simulate_publish(mqtt_client, topic)
