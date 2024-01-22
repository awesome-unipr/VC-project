import python_weather
import json
import asyncio
import os
import paho.mqtt.client as mqtt
from aiohttp import web


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
        print(msg.topic + " " + str(msg.payload))

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
    def __init__(self, mqtt_client, port):
        self.app = web.Application()
        self.routes = web.RouteTableDef()
        self.port = port
        self.mqtt_client = mqtt_client

        @self.routes.post("/weathercurrent")
        async def post_handler(request):
            data_curr = await request.post()
            print(data_curr)
            current_weather = {}

            current_weather["city"] = str(data_curr["current_city"])
            current_weather["temperature"] = str(data_curr["current_temperature"])
            current_weather["weather"] = str(data_curr["current_kind"])

            broad_msg = json.dumps(current_weather)

            self.mqtt_client.publish("vc2324/weather-current", broad_msg)

            return web.Response(text="ok")

        @self.routes.post("/weatherforecast")
        async def post_handler1(request):
            data = await request.json()
            data_forec = json.loads(data)
            print(data)
            forecast_weather = {}

            for i in data_forec:
                row = {}
                row["time"] = str(data_forec[i]["time"])
                row["temperature"] = str(data_forec[i]["temperature"])
                row["weather"] = str(data_forec[i]["kind"])
                forecast_weather[i] = row

            broad_msg = json.dumps(forecast_weather)

            self.mqtt_client.publish("vc2324/weather-forecast", broad_msg)

            return web.Response(text="ok")

        self.app.add_routes(self.routes)

    def start(self):
        web.run_app(self.app, port=self.port)

    def stop(self):
        web.run_app(self.app)




try:
    with open("Config.json", "r") as file:
        config_file = json.load(file)

    for o in config_file["Obu"]:
        if o["name"] == "Weather Information":
            http_server_port = o["http_port"]
            client_id = o["mqtt_id"]

    for b in config_file["MqttBroker"]:
        broker_ip = b["ip"]
        broker_port = b["port"]

    mqtt_client = MqttClient(broker_ip, broker_port, client_id)

    http_server = HttpServer(mqtt_client, http_server_port)

    mqtt_client.subscribe("vc2324/weather-current")
    mqtt_client.subscribe("vc2324/weather-forecast")
    mqtt_client.start()
    http_server.start()

    mqtt_client.stop()

    print("Program terminated!")
except Exception as e:
    raise e
