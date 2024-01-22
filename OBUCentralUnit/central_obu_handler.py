import paho.mqtt.client as mqtt
from aiohttp import web
import json
import re


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
        data = msg.payload.decode()

        cobu_handler.obu_status(msg.topic, str(data))

        match msg.topic:
            case "vc2324/radio":
                print("New message from: " + msg.topic + " - " + str(data))

            case "vc2324/weather-current":
                print("New message from: " + msg.topic + " - " + str(data))
                data = json.loads(msg.payload)
                if (
                    data["weather"] == "Rainy"
                    or data["weather"] == "Snowy"
                    or data["weather"] == "Misty"
                    or data["weather"] == "Stormy"
                ):
                    cobu_handler.set_weather_risk(2)
                else:
                    cobu_handler.set_weather_risk(0)

                cobu_handler.check_risk_level()

            case "vc2324/weather-forecast":
                print("New message from: " + msg.topic + " - " + str(data))

            case "vc2324/dms":
                print("New message from: " + msg.topic + " - " + str(data))
                if data == "Normal" or data == "Hungry" or data == "Bored":
                    cobu_handler.set_dms_risk(0)
                elif (
                    data == "Drunk"
                    or data == "Sleepy"
                    or data == "Dizzy"
                    or data == "Unpresent"
                ):
                    cobu_handler.set_dms_risk(3)
                else:
                    cobu_handler.set_dms_risk(1)

                cobu_handler.check_risk_level()

            case "vc2324/alert/brake":
                print("New message from: " + msg.topic + " - " + str(data))

            case "vc2324/alert/key-not-recognized":
                print("New message from: " + msg.topic + " - " + str(data))

            case "vc2324/key-is-ok":
                print("New message from: " + msg.topic + " - " + str(data))

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
    def __init__(self, cobu_handler, port):
        self.app = web.Application()
        self.routes = web.RouteTableDef()
        self.cobu_handler = cobu_handler
        self.port = port

        @self.routes.get("/vehicle-status")
        async def get_handler(request):
            status = self.cobu_handler.display_status()
            return web.json_response(status)

        self.app.add_routes(self.routes)

    def start(self):
        web.run_app(self.app, port=self.port)

    def stop(self):
        web.run_app(self.app)


class CobuHandler:
    def __init__(self, mqtt_client):
        self._mqtt_client = mqtt_client

        self.status = json.loads(
            '{"Obu": [\
            {"name": "radio", "status":"Default"},\
            {"name": "weather-current", "status":"Default"},\
            {"name": "weather-forecast", "status":"Default"},\
            {"name": "dms", "status":"Default"},\
            {"name": "brake", "status":"Default"},\
            {"name": "key-is-ok", "status":"Default"},\
            {"name": "key-not-recognized", "status":"Default"}\
            ]}'
        )

        self.risk_level = [0, 0]  # wheater and dms risk level

    def set_weather_risk(self, value):
        self.risk_level[0] = value

    def set_dms_risk(self, value):
        self.risk_level[1] = value

    def check_risk_level(self):
        risk_level = self.risk_level[0] + self.risk_level[1]
        # print(risk_level)
        if risk_level >= 3:
            if self.status["Obu"][4]["status"] != "Alert":
                self._mqtt_client.publish("vc2324/alert/brake", "Alert")
        else:
            if self.status["Obu"][4]["status"] != "Default":
                self._mqtt_client.publish("vc2324/alert/brake", "Default")

    def obu_status(self, topic, payload):
        for o in self.status["Obu"]:
            if re.search(o["name"], topic):
                o["status"] = payload

    def display_status(self):
        return self.status




try:
    with open("Config.json", "r") as file:
        config_file = json.load(file)

# BROKER SETTINGS
    for b in config_file["MqttBroker"]:
        broker_ip = b["ip"]
        broker_port = b["port"]

# HTTP SETTINGS
    for o in config_file["Obu"]:
        if o["name"] == "Central Unit":
            http_server_port = o["http_port"]
            client_id = o["mqtt_id"]

# CLASSES ISTANCES
    mqtt_client = MqttClient(broker_ip, broker_port, client_id)
    cobu_handler = CobuHandler(mqtt_client)
    http_server = HttpServer(cobu_handler, http_server_port)

# CLIENT SUBSRIPTIONS
    mqtt_client.subscribe("vc2324/radio")
    mqtt_client.subscribe("vc2324/weather-current")
    mqtt_client.subscribe("vc2324/weather-forecast")
    mqtt_client.subscribe("vc2324/dms")
    mqtt_client.subscribe("vc2324/alert/brake")
    mqtt_client.subscribe("vc2324/alert/key-not-recognized")
    mqtt_client.subscribe("vc2324/key-is-ok")

# START LOOP
    mqtt_client.start()
    http_server.start()
    mqtt_client.stop()
    print("Program terminated!")
except Exception as e:
    raise e
