import os
import sys
import time
import uuid
import ssl
import configparser
import json
import threading
from abc import ABCMeta, abstractmethod
import requests
import pickle
from paho.mqtt import client as mqtt_client


class MqttJwtToken:

    TOKEN_OBJ_NAME = 'newiot.jwt'

    def __init__(self, config_ini):

        con = configparser.ConfigParser()
        con.read(config_ini, encoding='utf-8')
        broker = dict(con.items('broker'))
        device = dict(con.items('device'))

        parameters = {**broker, **device}
        if type(parameters['tls'] == str):
            parameters['tls'] = False if parameters['tls'].lower() == 'false' else True
        parameters['port'] = int(parameters['port'])

        self.host = parameters['host']
        self.port = parameters['port']
        self.tls = parameters['tls']
        self.register_username = parameters['register_username']
        self.register_password = parameters['register_password']
        self.refresh_jwt_username = parameters['refresh_jwt_username']
        self.refresh_jwt_password = parameters['refresh_jwt_password']

        if 'client_id' not in parameters or parameters['client_id'] is None:
            self.client_id = str(uuid.uuid1())
        else:
            self.client_id = parameters['client_id']

        self.register_topic_sub = f'lass/dt/register/{parameters["product_key"]}/{parameters["device_sn"]}'
        self.register_topic_pub = f'lass/cmd/register/{parameters["product_key"]}/{parameters["device_sn"]}'

        self.refresh_topic_sub = f'lass/dt/jwt/refresh/{parameters["product_key"]}/{parameters["device_sn"]}'
        self.refresh_topic_pub = f'lass/cmd/jwt/refresh/{parameters["product_key"]}/{parameters["device_sn"]}'

        self.on_success = None

    def on_connect(self, m_client, userdata, flags, rc):
        if rc == 0:
            # print(f'Connected to MQTT Broker {self.host} as {self.client_id}! userdata: {userdata}')
            if userdata['action'] == 'register':
                print('Start registering...')
                m_client.publish(self.register_topic_pub, payload=json.dumps({"get_jwt": 1}))

            if userdata['action'] == 'refresh':
                print('Start refreshing...')
                token = self.get_token()
                payload = {'refresh': token['refresh']}
                m_client.publish(self.refresh_topic_pub, payload=json.dumps(payload))
        else:
            print(f'Failed to connect, return code: {rc}, maybe authorization server return 403.')

    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnect from {self.host}:{self.port}')
        print(f'Disconnection returned result: {rc}, userdata: {userdata}')

    def on_message(self, m_client, userdata, msg):
        # print(f"Received {msg.payload.decode()} from {msg.topic} topic qos {msg.qos} {msg.retain}")
        if userdata['action'] == 'register' or userdata['action'] == 'refresh':
            m_client.disconnect()
            # print(f'Retrieved token ({userdata}), disconnect token request.')
            token_obj = json.loads(msg.payload.decode())
            token_obj['create_cache_time'] = int(time.time())
            token_obj['tls'] = self.tls
            token_obj['host'] = self.host
            token_obj['port'] = self.port
            token_file = open(self.TOKEN_OBJ_NAME, 'wb')
            pickle.dump(token_obj, token_file)
            token_file.close()

            # print(f'Token is cached: {token_obj}')
            m_client.loop_stop(force=False)
            if self.on_success is not None:
                self.on_success(token_obj)

            timer = threading.Timer(token_obj['access_lifetime'], self.retrieving)
            timer.start()

    def retrieving(self):

        token = self.get_token()
        if token is not None:
            time_delta_sec = int(time.time()) - token['create_cache_time']

            if time_delta_sec >= token['access_lifetime']:
                if time_delta_sec >= token['refresh_lifetime']:
                    print(f'\033[31mRefresh_token expired! please register device again, then try again.\033[0m')
                    print(f'\033[31mBefore registering device, clean jwt cache first: python -m newiotclient clean\033[0m')
                    try:
                        sys.exit(0)
                    except Exception as e:
                        print(f'Refresh_token expired! {str(e)}')
                else:
                    self.__sub({'action': 'refresh'})
            else:
                if self.on_success is not None:
                    self.on_success(token)
        else:
            self.__sub({'action': 'register'})

    def __sub(self, userdata):
        if userdata['action'] == 'register':
            username = self.register_username
            password = self.register_password
            sub_topic = self.register_topic_sub
        elif userdata['action'] == 'refresh':
            username = self.refresh_jwt_username
            password = self.refresh_jwt_password
            sub_topic = self.refresh_topic_sub
        else:
            raise ValueError('jwt action error')

        client = mqtt_client.Client(self.client_id)
        client.reinitialise(client_id=self.client_id, clean_session=True, userdata=userdata)
        client.username_pw_set(username, password)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        if self.tls:
            client.tls_set(self.get_cert_file(), tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(True)
        client.connect(host=self.host, port=self.port)
        # print(f'Sub topic: {sub_topic} userdata: {userdata}')
        client.subscribe(sub_topic)
        client.loop_forever()

    @staticmethod
    def get_cert_file():
        return f'{os.path.abspath(os.path.dirname(__file__))}/cert/ca-bundle.crt'

    @classmethod
    def get_token(cls):
        try:
            token_file = open(cls.TOKEN_OBJ_NAME, 'rb')
            token = pickle.load(token_file)
            token_file.close()
            return token
        except (FileNotFoundError, EOFError):
            return None

    @classmethod
    def clean_token(cls):
        try:
            os.remove(cls.TOKEN_OBJ_NAME)
            print('Local JWT deleted!')
        except FileNotFoundError:
            print('No local JWT yet!')


class JwtMqttClient(threading.Thread, metaclass=ABCMeta):
    def __init__(self, **callbacks):
        super().__init__()
        self.no_response_sub = []  # Not responded id list
        self.callbacks = callbacks
        self.token = MqttJwtToken.get_token()
        self.client = self.mqtt_connect()

    def mqtt_connect(self):

        client = mqtt_client.Client()
        is_tls = self.token['tls']
        if is_tls:
            client.tls_set(MqttJwtToken.get_cert_file(), tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(True)
        client.username_pw_set(self.token['access'], 'jwt')

        # callback functions
        client.on_connect = self.on_connect if 'on_connect' not in self.callbacks else self.callbacks['on_connect']
        client.on_disconnect = self.on_disconnect if 'on_disconnect' not in self.callbacks else self.callbacks['on_disconnect']
        client.on_message = self.on_message if 'on_message' not in self.callbacks else self.callbacks['on_message']
        client.on_subscribe = self.on_subscribe if 'on_subscribe' not in self.callbacks else self.callbacks['on_subscribe']
        client.on_publish = self.on_publish if 'on_publish' not in self.callbacks else self.callbacks['on_publish']

        client.connect(host=self.token['host'], port=self.token['port'])

        return client

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print(f'Connection returned with result code: {rc}')

    @staticmethod
    def on_message(client, userdata, msg):
        print(f'Received message, topic: {msg.topic} payload: {msg.payload.decode()}')

    @staticmethod
    def on_disconnect(client, userdata, rc):
        print(f'Disconnection returned result: {rc}')

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.no_response_sub.remove(mid)

    @staticmethod
    def on_publish(client, userdata, mid):
        print(f'Published {mid}')

    def end(self):
        self.client.disconnect()
        self.client.loop_stop()


class JwtMqttClientSub(JwtMqttClient):

    def __init__(self, topic, **callbacks):
        super().__init__(**callbacks)
        self.topic = topic

    def run(self):
        # multiple topics: [('topic1', 0), ('topic2', 0)]
        result, mid = self.client.subscribe(self.topic)
        self.no_response_sub.append(mid)
        self.client.loop_forever()


class JwtMqttClientPub(JwtMqttClient):
    def __init__(self, topic, payload, **callbacks):
        super().__init__(**callbacks)
        self.topic = topic
        self.payload = payload

    def run(self):
        self.client.publish(topic=self.topic, payload=self.payload)

