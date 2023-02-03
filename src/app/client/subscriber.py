import paho.mqtt.client as mqtt
import json
from app.core.config import env


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(env("MQTT_BROKER_LAUNCH_TASK_TOPIC"))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == env("MQTT_BROKER_LAUNCH_TASK_TOPIC"):
        payload = json.loads(msg.payload)

        bucket_hash = payload["bucket_hash"]
        politic_name = payload["politic_name"]
        workflow_name = payload["workflow_name"]

        print(bucket_hash, politic_name, workflow_name)
        # TODO:
        # match politic_name:
        #     case "":
        #         reserve() # type: ignore
        #     case _:
        #         reserve() # type: ignore


def update_status(message):
    client.publish(env("MQTT_BROKER_STATUS_TASK_TOPIC"), message)


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    env("MQTT_BROKER_ADDRESS"),
    env("MQTT_BROKER_PORT"),
    60,
)

client.loop_forever()
