
import aiohttp
import asyncio
import datetime
import json
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from random import randint
from Gui import ControlGui
from OBUBrakingSystem import MqttBrakingSystem, BrakingHandler


if __name__ == '__main__':
    MQTT_BROKER = "test.mosquitto.org"
    MQTT_PORT = 1883

    mqtt_client = MqttBrakingSystem(MQTT_BROKER, MQTT_PORT)
    braking_handler = BrakingHandler(mqtt_client)

    mqtt_client.subscribe("vc2324/alert/brake")
    mqtt_client.subscribe("vc2324/alert/key-not-recognized")
    mqtt_client.subscribe("vc2324/key-is-ok")
    mqtt_client.start()


    with open("Config.json", "r") as file:
        config_file = json.load(file)

    for o in config_file["Obu"]:
        if o["name"] == "Infotainment System":
            info_port = o["http_port"]
        if o["name"] == "Weather Information":
            weather_port = o["http_port"]
        if o["name"] == "Central Unit":
            central_port = o["http_port"]
        if o["name"] == "Remote Keyless System":
            keyless_port = o["http_port"]

    gui = TkinterGui()
    vehicle = VehicleStatus(gui, central_port, keyless_port)
    radio = InfotainmentSystem(gui, info_port)
    meteo = WeatherInformation(gui, weather_port)
    dms = DriverMonitoringSystem(gui)
    rks = RemoteKeylessSystem(gui, keyless_port)

    gui.start_main_loop()
