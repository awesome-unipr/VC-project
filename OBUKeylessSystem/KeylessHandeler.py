import json

import paho.mqtt.client as mqtt
from aiohttp import web

# CONFIGURATION
with open("Config.json", "r") as file:
    config_file = json.load(file)

for o in config_file["Obu"]:
    if o["name"] == "Remote Keyless System":
        HTTP_PORT = o["http_port"]
        CLIENT_ID = o["mqtt_id"]
        MQTT_TOPIC = "vc2324/key-is-ok"

for b in config_file["MqttBroker"]:
    MQTT_BROKER = b["name"]
    MQTT_IP = b["ip"]
    MQTT_PORT = b["port"]

USER_ONE = {
    "identity": config_file["Driver"][0]["identity"],
    "sequence": config_file["Driver"][0]["sequence"],
}

USER_TWO = {
    "identity": config_file["Driver"][1]["identity"],
    "sequence": config_file["Driver"][1]["sequence"],
}

LAST_KEY = ""

WARNING = ""

STATUS = {"logged_in": 0}

mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    """
    Callback function for mqtt client connection
    """
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """
    Callback function for mqtt client message
    """
    print(msg.topic + " " + str(msg.payload))


def on_disconnect(client, userdata, rc):
    """
    Callback function for mqtt client disconnect
    """
    print("Disconnected with result code " + str(rc))


def on_publish(client, userdata, mid):
    """
    Callback function for mqtt client publish
    """
    print("Message " + str(mid) + " published")


def on_subscribe(client, userdata, mid, granted_qos):
    """
    Callback function for mqtt client subscribe
    """
    print("Subscribed to topic " + MQTT_TOPIC)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish = on_publish
mqtt_client.on_subscribe = on_subscribe


async def keyless_handler(request):
    """
    Http handler function for /keyless post route
    """
    global LAST_KEY
    global WARNING

    try:
        data = await request.json()
        identity = data.get("identity")
        sequence = data.get("sequence")

        if (
            str(identity) == USER_ONE["identity"]
            and str(sequence) == USER_ONE["sequence"]
        ):
            mqtt_client.publish(MQTT_TOPIC, "VALID KEY")
            LAST_KEY = identity
            STATUS["logged_in"] = 1
            return web.json_response(
                {"message": "VALID KEY: " + str(identity)}, status=200
            )

        if (
            str(identity) == USER_TWO["identity"]
            and str(sequence) == USER_TWO["sequence"]
        ):
            mqtt_client.publish(MQTT_TOPIC, "VALID KEY")
            LAST_KEY = identity
            STATUS["logged_in"] = 1
            return web.json_response(
                {"message": "VALID KEY: " + str(identity)}, status=200
            )

        WARNING = "UNRECOGNIZED KEY"
        return web.json_response({"error": "Invalid key"}, status=401)

    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid json"}, status=400)


async def driver_handler(request):
    """
    Http handler function for /driver get route
    """
    global LAST_KEY
    global WARNING

    print("KEY INFO: " + LAST_KEY + " - " + WARNING)
    if LAST_KEY in [USER_ONE["identity"], USER_TWO["identity"]] or LAST_KEY == "":
        return web.json_response(
            {"message": LAST_KEY, "warning": WARNING, "status": STATUS["logged_in"]},
            status=200,
        )

    return web.json_response({"error": "unauthorized"}, status=200)


async def logout_handler(request):
    """
    Http handler function for /logout get route

    Check if the user is authorized to logout
    and clear the LAST_KEY
    """
    global LAST_KEY
    global WARNING

    try:
        data = await request.json()
        identity = data.get("identity")
        sequence = data.get("sequence")

        if (
            str(identity) == USER_ONE["identity"]
            and str(sequence) == USER_ONE["sequence"]
        ):
            mqtt_client.publish(MQTT_TOPIC, "NO KEY")
            LAST_KEY = ""
            WARNING = ""
            STATUS["logged_in"] = 0
            return web.json_response({"message": "Logout successfully"}, status=200)

        if (
            str(identity) == USER_TWO["identity"]
            and str(sequence) == USER_TWO["sequence"]
        ):
            mqtt_client.publish(MQTT_TOPIC, "NO KEY")
            LAST_KEY = ""
            WARNING = ""
            STATUS["logged_in"] = 0
            return web.json_response({"message": "Logout successfully"}, status=200)

        # LAST_KEY.append("INVALID KEY")
        return web.json_response({"error": "Invalid key"}, status=401)

    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid json"}, status=400)


httpServer = web.Application()
httpServer.router.add_post("/keyless", keyless_handler)
httpServer.router.add_get("/driver", driver_handler)
httpServer.router.add_post("/logout", logout_handler)


if __name__ == "__main__":
    mqtt_client.connect(MQTT_IP, MQTT_PORT, 60)
    mqtt_client.loop_start()
    web.run_app(httpServer, port=HTTP_PORT)
