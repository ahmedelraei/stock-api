import paho.mqtt.client as mqtt
import json
from .models.stock import Stock
from .config import settings


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(settings.MQTT_TOPIC)


def on_message(client, userdata, msg):
    stock_data = json.loads(msg.payload.decode("utf-8"))
    Stock.create_or_update(**stock_data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
