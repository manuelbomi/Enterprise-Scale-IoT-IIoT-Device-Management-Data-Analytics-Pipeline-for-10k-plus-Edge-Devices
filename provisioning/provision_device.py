# Here's a complete version of provision_device.py — a Python script that automates fleet provisioning for IoT devices using claim certificates, AWS IoT Core, and Fleet Provisioning by Claim.
# This script is designed to be run on each device at first boot (e.g., Raspberry Pi), using a shared claim certificate and its own unique serial number to provision itself.
# Example usage:   python provisioning/provision_device.py --serial rpi-0042

#This will:

#Connect to AWS IoT Core using the claim certificate

#Publish a provisioning request to the template

#Receive a new cert/key for the device

#Save them under certs/<thing-name>-certificate.pem.crt etc.


import json
import time
import uuid
import ssl
import boto3
import argparse
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# ---------- CONFIGURABLE ----------
CLAIM_CERT = "certs/claim_cert.pem"
CLAIM_KEY = "certs/claim_private.key"
ROOT_CA = "certs/AmazonRootCA1.pem"

IOT_ENDPOINT = "<your-iot-endpoint>.amazonaws.com"  # Replace with your AWS IoT endpoint
TEMPLATE_NAME = "FleetProvisioningTemplate"
THING_GROUP = "group1"  # Or dynamically assign
REGION = "us-west-2"
# -----------------------------------

def get_device_serial():
    """Generate or retrieve a unique device ID (e.g., MAC, serial number)"""
    return str(uuid.uuid4())[:8]  # You can use a real device serial if available

def create_mqtt_client(client_id):
    """Creates an MQTT client using claim credentials"""
    client = AWSIoTMQTTClient(client_id)
    client.configureEndpoint(IOT_ENDPOINT, 8883)
    client.configureCredentials(ROOT_CA, CLAIM_KEY, CLAIM_CERT)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)
    return client

def provision_device(device_serial, mqtt_client):
    """Publish a provisioning request using Fleet Provisioning by Claim"""
    topic = "$aws/provisioning-templates/{}/provision/json".format(TEMPLATE_NAME)

    payload = {
        "parameters": {
            "SerialNumber": device_serial,
            "ThingGroup": THING_GROUP
        }
    }

    # Callback to handle response
    def callback(client, userdata, message):
        response = json.loads(message.payload.decode())
        print("\n Provisioning response received:")
        print(json.dumps(response, indent=2))

        # Save new certs
        cert = response["certificatePem"]
        key = response["privateKey"]
        ca = response["rootCa"]  # Optional

        thing_name = response["thingName"]

        with open(f"certs/{thing_name}-certificate.pem.crt", "w") as f:
            f.write(cert)
        with open(f"certs/{thing_name}-private.pem.key", "w") as f:
            f.write(key)

        print(f"\n Saved cert and key for: {thing_name}")
        exit(0)

    # Subscribe to accepted response
    resp_topic = "$aws/provisioning-templates/{}/provision/json/accepted".format(TEMPLATE_NAME)
    mqtt_client.subscribe(resp_topic, 1, callback)

    print(" Publishing provisioning request...")
    mqtt_client.publish(topic, json.dumps(payload), 1)

    # Wait for provisioning response
    while True:
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serial", help="Unique device serial number", required=False)
    args = parser.parse_args()

    serial_number = args.serial or get_device_serial()
    print(f" Using serial number: {serial_number}")

    mqtt_client = create_mqtt_client(client_id=serial_number)
    print(" Connecting using claim certificate...")
    mqtt_client.connect()

    provision_device(serial_number, mqtt_client)
