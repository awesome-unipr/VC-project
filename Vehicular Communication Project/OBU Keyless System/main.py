import json

import paho.mqtt.client as mqtt
from aiohttp import web

HTTP_PORT = 8888
MQTT_BROKER = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_TOPIC = 'vc2023/key-is-ok'

USER_ONE = {
    "identity": "1",
    "sequence": '123',
}

USER_TWO = {
    "identity": "2",
    "sequence": '456',
}


LAST_KEY = []
STATUS = {
    "logged_in": 0
}


mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """
    Callback function for mqtt client connection
    """
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """
    Callback function for mqtt client message
    """
    print(msg.topic + ' ' + str(msg.payload))

def on_disconnect(client, userdata, rc):
    """
    Callback function for mqtt client disconnect
    """
    print('Disconnected with result code ' + str(rc))

def on_publish(client, userdata, mid):
    """
    Callback function for mqtt client publish
    """
    print('Message ' + str(mid) + ' published')

def on_subscribe(client, userdata, mid, granted_qos):
    """
    Callback function for mqtt client subscribe
    """
    print('Subscribed to topic ' + MQTT_TOPIC)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish = on_publish
mqtt_client.on_subscribe = on_subscribe

async def keyless_handler(request):
    """
    Http handler function for /keyless post route
    """

    try:

        data = await request.json()
        identity = data.get('identity')
        sequence = data.get('sequence')

        if str(identity) == USER_ONE['identity'] and str(sequence) == USER_ONE['sequence']:
            mqtt_client.publish(MQTT_TOPIC, 'VALID KEY: ' + str(identity))
            LAST_KEY.append(identity)
            STATUS['logged_in'] = 1
            return web.json_response({'message': 'VALID KEY: ' + str(identity)}, status=200)

        if str(identity) == USER_TWO['identity'] and str(sequence) == USER_TWO['sequence']:
            mqtt_client.publish(MQTT_TOPIC, 'VALID KEY: ' + str(identity))
            LAST_KEY.append(identity)
            STATUS['logged_in'] = 1
            return web.json_response({'message': 'VALID KEY: ' + str(identity)}, status=200)


        LAST_KEY.append("INVALID")
        return web.json_response({'error': 'Invalid key'}, status=401)

    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid json'}, status=400)





async def driver_handler(request):
    """
    Http handler function for /driver get route
    """

    if len(LAST_KEY) == 0:
        return web.json_response({'error': 'No available latest access'}, status=200)

    if LAST_KEY[-1] in [USER_ONE['identity'], USER_TWO['identity']]:
        return web.json_response({'message': 'Last identity: ' + str(LAST_KEY[-1])}, status=200)


    return web.json_response({'error': 'unauthorized'}, status=200)


async def logout_handler(request):
    """
    Http handler function for /logout get route

    Check if the user is authorized to logout
    and clear the LAST_KEY 
    """
    try:
        data = await request.json()
        identity = data.get('identity')
        sequence = data.get('sequence')

        if str(identity) == USER_ONE['identity'] and str(sequence) == USER_ONE['sequence']:
            mqtt_client.publish(MQTT_TOPIC, 'VALID KEY: ' + str(identity))
            LAST_KEY.append(identity)
            STATUS['logged_in'] = 0
            return web.json_response({'message': 'VALID KEY: ' + str(identity)}, status=200)

        if str(identity) == USER_TWO['identity'] and str(sequence) == USER_TWO['sequence']:
            mqtt_client.publish(MQTT_TOPIC, 'VALID KEY: ' + str(identity))
            LAST_KEY.append(identity)
            STATUS['logged_in'] = 0
            return web.json_response({'message': 'VALID KEY: ' + str(identity)}, status=200)


        LAST_KEY.append("INVALID")
        return web.json_response({'error': 'Invalid key'}, status=401)

    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid json'}, status=400)


httpServer = web.Application()
httpServer.router.add_post('/keyless', keyless_handler)
httpServer.router.add_get('/driver', driver_handler)
httpServer.router.add_post('/logout', logout_handler)



if __name__ == '__main__':
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_start()
    web.run_app(httpServer, port=HTTP_PORT)
