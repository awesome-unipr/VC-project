import paho.mqtt.client as mqtt
from aiohttp import web
from random import randint
import time
import threading
import json


class MqttClient:
    def __init__(self, host, port, id):
        self.client = mqtt.Client(client_id=id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.host = host
        self.port = port

        self.mqtt_connection()

    def mqtt_connection(self):
        self.client.connect(self.host, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        return 0

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Subscribed to " + topic)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()


class HttpServer:
    def __init__(self, dms_handler, port):
        self.app = web.Application()
        self.routes = web.RouteTableDef()
        self.port = port

        self.dms_handler = dms_handler

        @self.routes.get("/dms")
        async def get_handler(request):
            status = self.dms_handler.display_status()
            return web.Response(text=status)

        self.app.add_routes(self.routes)

    def start(self):
        web.run_app(self.app, port=self.port)

    def stop(self):
        web.run_app(self.app)


class DmsHandler:
    def __init__(self, mqtt_client):
        self._mqtt_client = mqtt_client
        self._current_status = "Normal"

    def change_status(self):
        status = [
            "Angry",
            "Tired",
            "Drunk",
            "Distracted",
            "Normal",
            "Bored",
            "Hungry",
            "Sleepy",
            "Dizzy",
            "Unpresent",
        ]
        n = randint(0, 9)
        new_status = status[n]
        self._current_status = new_status
        self._mqtt_client.publish("vc2324/dms", new_status)
        print(new_status)

    def display_status(self):
        return self._current_status


try:
    with open("Config.json", "r") as file:
        config_file = json.load(file)

    for o in config_file["Obu"]:
        if o["name"] == "Driver Monitoring System":
            http_server_port = o["http_port"]
            client_id = o["mqtt_id"]

    for b in config_file["MqttBroker"]:
        broker_ip = b["ip"]
        broker_port = b["port"]

    mqtt_client = MqttClient(broker_ip, broker_port, client_id)
    dms_handler = DmsHandler(mqtt_client)
    http_server = HttpServer(dms_handler, http_server_port)

    mqtt_client.subscribe("vc2324/dms")
    mqtt_client.start()

    # Start the thread for changing the status
    def change_status_thread():
        while True:
            dms_handler.change_status()
            time.sleep(2)

    change_status_thread = threading.Thread(target=change_status_thread)
    change_status_thread.start()

    http_server.start()

    mqtt_client.stop()
except Exception as e:
    raise e
